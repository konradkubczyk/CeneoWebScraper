from app.utils import get_item
from app.parameters import selectors

class Opinion():
    def __init__(self, opinion_id="", author="", recommendation=None, stars=0, content="", useful=0, useless=0, published=None, purchased=None, pros=[], cons=[]):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.useful = useful
        self.useless = useless
        self.published = published
        self.purchased = purchased
        self.pros = pros
        self.cons = cons
        return self

    def extract_opinion(self, opinion):
        for key, value in selectors.items():
            setattr(self, key, get_item(opinion, *value))
        self.opinion_id = opinion["data-entry-it"]
        return self

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def to_dict(self) -> dict:
        pass