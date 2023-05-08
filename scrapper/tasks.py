from . import utils, models

def scrape_news(sites):
    """
    Scrape news from news sites

    Args:
        sites (list): list of news sites url
    """
    sites = sites or ["https://www.nytimes.com/", "https://edition.cnn.com/", "https://www.bbc.com/"]
    for website in sites:
        articles = utils.scrape_articles(website)
        models.Article.objects.bulk_create([models.Article(**article) for article in articles.values()])