from . import utils, models

def scrape_news():
    for website in ["https://www.nytimes.com/", "https://edition.cnn.com/"]:
        articles = utils.scrape_articles(website)
        models.Article.objects.bulk_create([models.Article(**article) for article in articles.values()])