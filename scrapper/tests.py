from django.test import TestCase
from django.conf import settings
import unittest
import requests
import os
import json

from .websites import cnn, nytimes, bbc
from . import utils

class CNNWebsiteTestCase(unittest.TestCase):
    def test_scrape_article_1(self):
        # resp = requests.get("https://edition.cnn.com/2023/05/07/uk/suella-braverman-profile-migration-gbr-intl/index.html")
        # with open(os.path.join(settings.BASE_DIR, "scrapper/data/cnn/article_1.txt"), "wb") as f:
        #     f.write(resp.content)
        with open(os.path.join(settings.BASE_DIR, "scrapper/data/cnn/article_1.txt"), "r") as f:
            content = f.read()
        article = cnn.CNNArticle(content)
        self.assertEqual(article.title, "‘A Trump tribute act’: Meet Suella Braverman, the commander-in-chief of Britain’s culture wars")
        self.assertEqual(article.authors, ["rob picheta"])
        self.assertEqual(article.published_at, "2023-05-07 12:33:00")

    def test_scrape_article_2(self):
        # resp = requests.get("https://edition.cnn.com/2023/05/07/football/son-heung-min-tottenham-hotspur-crystal-palace-premier-league-spt-intl/index.html")
        # with open(os.path.join(settings.BASE_DIR, "scrapper/data/cnn/article_2.txt"), "wb") as f:
        #     f.write(resp.content)
        with open(os.path.join(settings.BASE_DIR, "scrapper/data/cnn/article_2.txt"), "r") as f:
            content = f.read()
        article = cnn.CNNArticle(content)
        self.assertEqual(article.title, "Tottenham Hotspur and Crystal Palace condemn alleged racial abuse towards Son Heung-min during Premier League game")
        self.assertEqual(article.authors, ["george ramsay"])
        self.assertEqual(article.published_at, "2023-05-07 10:25:00")


class CNNWebsiteUtilTestCase(unittest.TestCase):
    def test_scrape_article_1(self):
        articles = utils.scrape_articles("https://edition.cnn.com/")
        with open(os.path.join(settings.BASE_DIR, "scrapper/data/cnn_1.json"), "w") as f:
            json.dump(articles, f, indent=4)
        self.assertNotEqual(articles, {})


class NYTWebsiteTestCase(unittest.TestCase):
    def test_scrape_article_1(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }
        # resp = requests.get("https://www.nytimes.com/2023/05/07/world/asia/south-korea-japan-summit-apology.html", headers=headers)
        # with open(os.path.join(settings.BASE_DIR, "scrapper/data/nytimes/article_1.txt"), "wb") as f:
        #     f.write(resp.content)
        with open(os.path.join(settings.BASE_DIR, "scrapper/data/nytimes/article_1.txt"), "r") as f:
            content = f.read()
        article = nytimes.NYTimesArticle(content)
        self.assertEqual(article.title, "Leaders of Japan and South Korea Vow to Deepen Ties")
        self.assertEqual(article.authors, ["choe sang-hun", "motoko rich"])
        self.assertEqual(article.published_at, "2023-05-07 12:28:47-04:00")

    def test_scrape_article_2(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }
        # resp = requests.get("https://www.nytimes.com/2023/05/07/world/canada/ken-sim-vancouver-china.html", headers=headers)
        # with open(os.path.join(settings.BASE_DIR, "scrapper/data/nytimes/article_2.txt"), "wb") as f:
        #     f.write(resp.content)
        with open(os.path.join(settings.BASE_DIR, "scrapper/data/nytimes/article_2.txt"), "r") as f:
            content = f.read()
        article = nytimes.NYTimesArticle(content)
        self.assertEqual(article.title, "Did China Help Vancouver’s Mayor Win Election?")
        self.assertEqual(article.authors, ["dan bilefsky"])
        self.assertEqual(article.published_at, "2023-05-07 05:00:32-04:00")

class NYTWebsiteUtilTestCase(unittest.TestCase):
    def test_scrape_article_1(self):
        articles = utils.scrape_articles("https://www.nytimes.com/")
        with open(os.path.join(settings.BASE_DIR, "scrapper/data/nytimes_1.json"), "w") as f:
            json.dump(articles, f, indent=4)
        self.assertNotEqual(articles, {})

class BBCWebsiteTestCase(unittest.TestCase):
    def test_scrape_article_1(self):
        # resp = requests.get("https://www.bbc.com/news/world-us-canada-65521233")
        # with open(os.path.join(settings.BASE_DIR, "scrapper/data/bbc/article_1.txt"), "wb") as f:
        #     f.write(resp.content)
        with open(os.path.join(settings.BASE_DIR, "scrapper/data/bbc/article_1.txt"), "r") as f:
            content = f.read()
        article = bbc.BBCArticle(content)
        self.assertEqual(article.title, "Brownsville: Eight dead as car strikes people in Texas border town")
        self.assertEqual(article.authors, ["kathryn armstrong"])
        self.assertEqual(article.published_at, "2023-05-07 21:18:51+00:00")

    def test_scrape_article_2(self):
        # resp = requests.get("https://www.bbc.com/news/world-asia-india-65409483")
        # with open(os.path.join(settings.BASE_DIR, "scrapper/data/bbc/article_2.txt"), "wb") as f:
        #     f.write(resp.content)
        with open(os.path.join(settings.BASE_DIR, "scrapper/data/bbc/article_2.txt"), "r") as f:
            content = f.read()
        article = bbc.BBCArticle(content)
        self.assertEqual(article.title, "SCO summit : Why peace talks are not on Bilawal Bhutto Zardari's agenda in India")
        self.assertEqual(article.authors, ["soutik biswas"])
        self.assertEqual(article.published_at, "2023-05-05 04:56:45+00:00")

class BBCWebsiteUtilTestCase(unittest.TestCase):
    def test_scrape_article_1(self):
        articles = utils.scrape_articles("https://www.bbc.com/")
        with open(os.path.join(settings.BASE_DIR, "scrapper/data/bbc_1.json"), "w") as f:
            json.dump(articles, f, indent=4)
        self.assertNotEqual(articles, {})