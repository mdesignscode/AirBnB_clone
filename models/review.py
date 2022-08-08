#!/usr/bin/python3
"""Review of User's Experience"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Review of User's Experience

    Args:
        place_id (string): it will be the Place.id
        user_id (string): it will be the User.id
        text (string) - user's review"""

    place_id = ''
    user_id = ''
    text = ''
