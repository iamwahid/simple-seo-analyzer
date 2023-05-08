from .base import BaseArticle
import dateutil.parser


class CNNArticle(BaseArticle):

    def _get_headline(self):
        return self.soup.find("h1", {"class": "story-body__h1"}).text.strip()

    def _get_title(self):
        def is_title(tag):
            if tag.name == "h1":
                return True
        return self.soup.find(is_title).text.strip()

    def _get_authors(self):
        def is_author(tag):
            tag1 = tag.name == "p" and tag.get("data-type") == "byline-area"
            tag2 = tag.name == "span" and "byline__name" in tag.get("class", [])
            if tag1 or tag2:
                return True
        return [author.text.strip().lower() for author in self.soup.findAll(is_author)]

    def _get_content(self):
        def is_content(tag):
            if tag.name == "div" and "article__content" in tag.get("class", []):
                return True
        return [content.text.strip() for content in self.soup.findAll(is_content)]

    def _parse_datetime(self, datetimestr):
        return dateutil.parser.parse(datetimestr)
    
    def _get_published_at(self):
        def is_published_at(tag):
            tag1 = tag.name == "div" and "article__published_at" in tag.get("class", [])
            tag2 = tag.name == "div" and "timestamp" in tag.get("class", [])
            if tag1 or tag2:
                return True
        
        published_at = None
        for content in self.soup.findAll(is_published_at):
            try:
                timestr = content.text.strip().split("\n")[1].strip()
                published_at = self._parse_datetime(timestr)
            except Exception as e:
                pass
        return str(published_at) if published_at else None