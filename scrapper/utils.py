import requests
from bs4 import BeautifulSoup
from datetime import datetime

from scrapper.models import Article

def insert_article(article):
    Article.objects.create()

def site_online(url):
    response = requests.get(url)
    return response.status_code == 200, response

def get_article_data(article):
    url = article.find('a', {'class': 'js-headline-text'}).text.strip()
    title = article.find('a', {'class': 'js-headline-text'}).text.strip()
    author = article.find('a', {'rel': 'author'}).text.strip()
    content = article.find('div', {'class': 'js-article__body'}).text.strip()
    published_at = datetime.strptime(article.find('time')['datetime'], '%Y-%m-%dT%H:%M:%SZ')
    return dict(url=url, title=title, author=author, content=content, published_at=published_at)

def is_article(tag):
    if tag.name == "a":
        url = tag.get("href", "")
        return url.endswith(".html") and not url.startswith("#") and not url.startswith("javascript")

def parse_site(url):
    online, response = site_online(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.findAll(is_article)

    for article in articles:
        data = get_article_data(article)
        insert_article(**data)
    
