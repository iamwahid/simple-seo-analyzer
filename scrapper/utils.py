import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from scrapper.models import Article
from scrapper.websites import cnn, nytimes
from seo import utils as seo_utils

def insert_article(article):
    Article.objects.create(**article)

def site_online(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200, response

def get_article_data(url, article_class):
    online, response = site_online(url)

    if not online:
        return False, None

    article = article_class(html_content=response.content)

    url = url
    title = article.title
    author = ", ".join(article.authors)
    content = article.content
    published_at = str(article.published_at)

    return True, dict(url=url, title=title, author=author, content=content, published_at=published_at)

def is_article_html(tag):
    if tag.name == "a":
        url = tag.get("href", "")
        return url.endswith(".html") and not url.startswith("#") and not url.startswith("javascript")

def get_article_class(base_url):
    if "cnn" in base_url:
        return cnn.CNNArticle
    elif "nytimes" in base_url:
        return nytimes.NYTimesArticle
    else:
        raise NotImplementedError(f"Article scrapping for {base_url} not supported")

def scrape_articles(url):
    online, response = site_online(url)
    proto = re.findall('(\w+)://', url)[0]
    base_url = url.replace(f"{proto}://", "").split("/")[0]
    soup = BeautifulSoup(response.content, 'html.parser')
    article_class = get_article_class(base_url)
    
    if article_class in [cnn.CNNArticle, nytimes.NYTimesArticle]:
        articles_url = [article.get("href") for article in soup.findAll(is_article_html)]
    else:
        raise NotImplementedError(f"Article scrapping for {base_url} not supported")

    for i, url in enumerate(articles_url):
        if seo_utils.is_relative_link(url):
            articles_url[i] = f"{proto}://{base_url}/{url}"
        elif seo_utils.is_root_link(url):
            articles_url[i] = f"{proto}://{base_url}{url}"
    
    articles = {}
    for url in articles_url[:10]:
        success, data = get_article_data(url, article_class)
        if success:
            articles[url] = data
    return articles
    
