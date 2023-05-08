import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from scrapper.websites import cnn, nytimes, bbc
from seo import utils as seo_utils


def site_online(url):
    """
    Check if site is online and return the response

    Args:
        url (str): website url

    Returns:
        tuple: online (bool), response (requests.models.Response)
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200, response

def get_article_data(url, article_class):
    """
    Get article data from url

    Args:
        url (str): article url
        article_class (scrapper.websites.BaseArticle): News Article class

    Returns:
        tuple: success (bool), article_data (dict)
    """

    online, response = site_online(url)

    if not online:
        return False, None

    article = article_class(html_content=response.content)

    url = url
    title = article.title
    author = ", ".join(article.authors)
    content = article.content
    published_at = article.published_at

    return True, dict(url=url, title=title, author=author, content=content, published_at=published_at)

def is_article_html(tag):
    """
    Check if element contains article html link
    """

    if tag.name == "a":
        url = tag.get("href", "")
        return url.endswith(".html") and not url.startswith("#") and not url.startswith("javascript")

def is_bbc_article_link(tag):
    """
    Check if element contains BBC's article link
    """
    if tag.name == "a":
        url = tag.get("href", "")
        reel = url.startswith("/reel")
        numeric_endings = re.findall(r"\d+$", url)
        return not reel and numeric_endings and not url.startswith("#") and not url.startswith("javascript")

def is_bbc_homepage_body(tag):
    """
    Check if element contains is BBC's homepage body
    """

    if tag.name == "div" and tag.get("id") == "orb-modules":
        return True

def get_article_class(base_url):
    """
    get Article class based on base url
    """

    if "cnn." in base_url:
        return cnn.CNNArticle
    elif "nytimes." in base_url:
        return nytimes.NYTimesArticle
    elif "bbc." in base_url:
        return bbc.BBCArticle
    else:
        raise NotImplementedError(f"Article scrapping for {base_url} not supported")

def scrape_articles(url):
    """
    Scrape all articles from url

    Args:
        url (str): website url

    Returns:
        list: list of article data
    """

    # check website is onlune
    online, response = site_online(url)
    if not online:
        raise Exception(f"Site {url} is not online")
    
    # get protocol and base url
    proto = re.findall('(\w+)://', url)[0]
    base_url = url.replace(f"{proto}://", "").split("/")[0]

    # prepare soup
    soup = BeautifulSoup(response.content, 'html.parser')
    # determine news article class based on base url
    article_class = get_article_class(base_url)

    # get all articles url based on article class
    if article_class in [cnn.CNNArticle, nytimes.NYTimesArticle]:
        articles_url = [article.get("href") for article in soup.findAll(is_article_html)]
    elif article_class in [bbc.BBCArticle]:
        _body_section = soup.find(is_bbc_homepage_body)
        articles_url = [article.get("href") for article in _body_section.findAll(is_bbc_article_link)]
    else:
        raise NotImplementedError(f"Article scrapping for {base_url} not supported")

    for i, url in enumerate(articles_url):
        if seo_utils.is_relative_link(url):
            articles_url[i] = f"{proto}://{base_url}/{url}"
        elif seo_utils.is_root_link(url):
            articles_url[i] = f"{proto}://{base_url}{url}"
    
    articles = {}
    # TODO: limit the articles to scrape
    for url in articles_url[:20]:
        success, data = get_article_data(url, article_class)
        if success:
            articles[url] = data
    return articles
    
