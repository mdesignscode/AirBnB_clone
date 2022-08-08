#!/usr/bin/python3
"""creates a user for the application"""

from base_model import BaseModel


class User(BaseModel):
    """creates a user for the application

        Attributes:
            email (string): empty string
            password (string): empty string
            first_name (string): empty string
            last_name (string): empty string
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
