# app/affirmation/domain/affirmation_entity.py
from datetime import datetime

class AffirmationEntity:
    """
    Represents an affirmation in the domain layer.
    """
    def __init__(self, id: str, title: str, content: str):
        self.id = id
        self.title = title
        self.content = content

    def update_content(self, title: str, content: str):
        """
        Example of a domain operation that modifies the state.
        """
        self.title = title
        self.content = content

