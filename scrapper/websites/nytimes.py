from .base import BaseArticle
import dateutil.parser


class NYTimesArticle(BaseArticle):
    def _get_title(self):
        def is_title(tag):
            if tag.name == "h1":
                return True
        tags = self.soup.findAll(is_title)
        title = tags[0].text.strip().strip(u"\u200b")
        return title

    def _get_authors(self):
        def is_author(tag):
            tag1 = tag.name == "p" and tag.get("data-type") == "byline-area"
            tag2 = tag.name == "span" and "css-1baulvz" in tag.get("class", []) and tag.get("itemprop") == "name"
            if tag2:
                return True
        return [author.text.strip().lower() for author in self.soup.findAll(is_author)]

    def _get_content(self):
        def is_content(tag):
            if tag.name == "section" and tag.get("name") == "articleBody":
                return True
        return [content.text.strip() for content in self.soup.findAll(is_content)]

    def _parse_datetime(self, datetimestr):
        return dateutil.parser.parse(datetimestr)
    
    def _get_published_at(self):
        def is_published_at_wrapper(tag):
            tag1 = tag.name == "div" and tag.get("data-testid") == "reading-time-module"
            if tag1:
                return True

        def is_published_at(tag):
            tag1 = tag.name == "time"
            if tag1:
                return True
        
        _published_at = None

        try:
            wrapper = self.soup.findAll(is_published_at_wrapper)[0]
            _published_at = wrapper.findAll(is_published_at)[0].get("datetime")
            _published_at = self._parse_datetime(_published_at)
        except Exception as e:
            pass

        return str(_published_at) if _published_at else None