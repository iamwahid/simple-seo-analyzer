from bs4 import BeautifulSoup

class BaseArticle:
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, "html.parser")

    @property
    def title(self):
        if not hasattr(self, "_get_title"):
            raise NotImplementedError("Subclasses should implement _get_title()")
        try:
            _title = self._get_title()
        except:
            _title = None
        return _title

    @property
    def authors(self):
        if not hasattr(self, "_get_authors"):
            raise NotImplementedError("Subclasses should implement _get_authors()")
        try:
            _authors = self._get_authors()
        except:
            _authors = None
        return _authors

    @property
    def content(self):
        if not hasattr(self, "_get_content"):
            raise NotImplementedError("Subclasses should implement _get_content()")
        try:
            _content = self._get_content()
        except:
            _content = None
        return _content
    
    @property
    def published_at(self):
        if not hasattr(self, "_get_published_at"):
            raise NotImplementedError("Subclasses should implement _get_published_at()")
        try:
            _published_at = self._get_published_at()
        except:
            _published_at = None
        return _published_at