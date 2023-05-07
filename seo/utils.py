from seoanalyzer import analyze
import requests
import re
from bs4 import BeautifulSoup
import concurrent.futures

def analyze_site(site, sitemap=None):
    if not sitemap:
        for _index in ["sitemap.xml", "sitemap", "sitemap_index.xml"]:
            _site = site if not site.endswith("/") else site[:-1]
            sitemap_url = f"{_site}/{_index}"
            try:
                response = requests.head(sitemap_url)
                if response.status_code == 200:
                    # print(f"status code: {response.status_code} {sitemap_url}")
                    sitemap = sitemap_url
                    break
            except Exception as e:
                print(f"Error: {e}")
                continue
    
    # handle if sitemap if causing error
    try:
        output = analyze(site, sitemap, follow_links=False)
    except Exception as e:
        output = analyze(site, follow_links=False)

    result = {}
    for page in output.get("pages", []):
        result["word_count"] = page.get("word_count", 0)
        result["title"] = page.get("title")
        _current_keywords = result.get("keywords", [])
        _current_keywords = _current_keywords + [word[1] for word in page.get("keywords", []) if word not in _current_keywords]
        result["keywords"] = _current_keywords

    result.update(parse_site(site))
    return result

def is_root_link(url):
    return not url.startswith("http") and url.startswith("/")

def is_relative_link(url):
    return not url.startswith("http") and not url.startswith("/")

def build_url(proto, base_url, url):
    if is_root_link(url):
        url = f"{proto}://{base_url}{url}"
    elif is_relative_link(url):
        url = f"{proto}://{base_url}/{url}"
    return url


def get_images(tag):
    if tag.name == "img":
        return True

def get_anchors(tag):
    if tag.name == "a":
        url = tag.get("href")
        return url and not url.startswith("#") and not url.startswith("javascript")

def get_metas(tag):
    if tag.name == "meta":
        return True

def is_internal(base_url, url):
    proto = re.findall('(\w+)://', url)[0]
    url = url.replace(f"{proto}://", "").split("/")[0]
    return url.startswith(base_url)

def is_active(proto, base_url, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }
    url = build_url(proto, base_url, url)

    code = requests.head(url, headers=headers).status_code
    if code != 200:
        code = requests.get(url, headers=headers).status_code
    return code == 200

def _process_meta(metas):
    _metas = {}
    for meta in metas:
        name = meta.get("name") if meta.get("name") else meta.get("property")
        if name:
            _metas[name.lower()] = meta.get("content")
    return _metas

def _process_anchor(proto, base_url, anchors):
    _urls = []
    for _url in anchors:
        _url = _url.get("href")
        if is_root_link(_url) or is_relative_link(_url):
            _url = build_url(proto, base_url, _url)
        _urls.append(_url)
    return _urls

def _process_url(proto, base_url, urls):
    _active_links = []
    futures = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _url in urls:
            futures[_url] = executor.submit(is_active, proto, base_url, _url)

    for _url, future in futures.items():
        if future.result():
            _active_links.append(_url)
    return _active_links

def parse_site(url):
    response = requests.get(url)
    
    res = BeautifulSoup(response.content, "html.parser")
    images = res.findAll(get_images)
    anchors = res.findAll(get_anchors)
    metas = _process_meta(res.findAll(get_metas))

    proto = re.findall('(\w+)://', url)[0]
    base_url = url.replace(f"{proto}://", "").split("/")[0]
    urls = _process_anchor(proto, base_url, anchors)
    _active_links = _process_url(proto, base_url, urls)

    dead_links = [link for link in urls if link not in _active_links]
    internal_links = [link for link in _active_links if is_internal(base_url, link)]
    external_links = [link for link in _active_links if link not in internal_links]
    no_alt_images = [str(image) for image in images if not image.get("alt")]

    return {
        "no_alt_images": no_alt_images,
        "dead_links": len(dead_links),
        "internal_links": len(internal_links),
        "external_links": len(external_links),
        "meta": metas,
        "keyword": metas.get("keywords", ""),
        "meta_description": metas.get("description"),
    }