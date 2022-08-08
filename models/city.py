#!/usr/bin/python3
"""The City User will be Visiting"""

from models.base_model import BaseModel


class City(BaseModel):
    """The City User will be Visiting

    Args:
        name (string): name of City
        state_id (string): id of state of City"""

    name = ""
    state_id = ""
