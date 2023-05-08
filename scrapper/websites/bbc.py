from .base import BaseArticle
import dateutil.parser

class BBCArticle(BaseArticle):
    def _get_title(self):
        def is_title(tag):
            if tag.name == "h1":
                return True
        return self.soup.find(is_title).text.strip()

    def _get_authors(self):
        def is_auther_wrapper(tag):
            tag1 = tag.name == "div" and tag.get("data-component") == "byline-block"
            return tag1

        def is_author(tag):
            classes = " ".join(tag.get("class", []))
            tag2 = tag.name == "div" and "TextContributorName" in classes
            return tag2

        _authors = []
        _wrapper = self.soup.find(is_auther_wrapper)
        if _wrapper:
            _authors = [author.text.lower().replace("by", "").strip() for author in _wrapper.findAll(is_author)]
        return _authors

    def _get_content(self):
        def is_content(tag):
            classes = " ".join(tag.get("class", []))
            if tag.name == "div" and tag.get("data-component") == "text-block" and "RichTextComponentWrapper" in classes:
                return True
        return [content.text.strip() for content in self.soup.findAll(is_content)]

    def _parse_datetime(self, datetimestr):
        return dateutil.parser.parse(datetimestr)
    
    def _get_published_at(self):
        def is_published_at(tag):
            tag1 = tag.name == "time" and tag.get("data-testid") == "timestamp"
            return tag1
        
        published_at = None
        for _timestamp in self.soup.findAll(is_published_at):
            _published_at = None
            try:
                timestr = _timestamp.get("datetime")
                _published_at = self._parse_datetime(timestr)
            except Exception as e:
                pass
            published_at = _published_at
        return str(published_at) if published_at else None