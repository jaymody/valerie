"""Data classes."""
import os
import logging

import bs4
import tldextract

from .preprocessing import clean_text

_logger = logging.getLogger(__name__)


class Claim:
    """A claim."""

    def __init__(
        self,
        id,
        claim,
        claimant=None,
        label=None,
        date=None,
        related_articles=None,
        explanation=None,
        support=None,
    ):
        """Constructor for Claim."""
        self.id = id
        self.claim = clean_text(claim)
        self.claimant = claimant
        self.label = label
        self.date = date
        self.related_articles = related_articles
        self.explanation = explanation
        self.support = support

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        if "id" in d:
            _id = d.pop("id")
            return cls(_id, **d)
        return cls(**d)


class Article:
    """An article."""

    def __init__(
        self,
        id,
        content=None,
        title=None,
        source=None,
        author=None,
        url=None,
        date=None,
    ):
        """Constructor for Article."""
        self.id = id
        self.title = title
        self.content = content
        self.source = tldextract.extract(url).domain if url else None
        self.author = author
        self.url = url
        self.date = date

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        if "id" in d:
            _id = d.pop("id")
            return cls(_id, **d)
        return cls(**d)

    @classmethod
    def from_txt(cls, id, text, **kwargs):
        """Construct an Article given text."""
        text = clean_text(text)
        return cls(id, content=text, **kwargs)

    @classmethod
    def from_html(cls, id, html, **kwargs):
        """Constructs an Article given an html text."""

        def tag_visible(element):
            whitelist = ["h1", "h2", "h3", "h4", "h5", "body", "p", "font"]
            if element.parent.name not in whitelist:
                return False
            if isinstance(element, bs4.Comment):
                return False
            return True

        soup = bs4.BeautifulSoup(html, "html.parser")
        texts = soup.findAll(text=True)
        texts = filter(tag_visible, texts)

        text = ""
        for t in texts:
            t = clean_text(t)
            if t and len(t) > 32:  # dissallow empty/short text sequences
                text += t + " "

        if "title" not in kwargs:
            title = soup.title if soup.title and soup.title.string else None
            title = clean_text(title.string) if title else None
        return cls(id, content=text, title=title, **kwargs)
