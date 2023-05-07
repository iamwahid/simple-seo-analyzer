from django.test import TestCase
import unittest
import requests

from .websites import bbc

class BBCWebsiteTestCase(unittest.TestCase):
    def test_scrape_article_1(self):
        resp = requests.get("https://edition.cnn.com/2023/05/07/uk/suella-braverman-profile-migration-gbr-intl/index.html")
        article = bbc.BBCArticle(resp.content)
        self.assertEqual(article.title, "‘A Trump tribute act’: Meet Suella Braverman, the commander-in-chief of Britain’s culture wars")
        self.assertEqual(article.authors, ["Rob Picheta"])
        self.assertEqual(article.published_at, "9:04 AM EDT, Sun May 7, 2023")

    def test_scrape_article_2(self):
        resp = requests.get("https://edition.cnn.com/2023/05/07/football/son-heung-min-tottenham-hotspur-crystal-palace-premier-league-spt-intl/index.html")
        article = bbc.BBCArticle(resp.content)
        self.assertEqual(article.title, "Tottenham Hotspur and Crystal Palace condemn alleged racial abuse towards Son Heung-min during Premier League game")
        self.assertEqual(article.authors, ["George Ramsay"])
        self.assertEqual(article.published_at, "10:25 AM EDT, Sun May 7, 2023")
