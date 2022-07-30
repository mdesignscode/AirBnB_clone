#!/usr/bin/python3
"""defines all common attributes/methods for other classes"""

from datetime import datetime
import uuid
from .__init__ import storage


class BaseModel:
    """defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """
        Sets:
            a unique id to each object,
            the time each object was created,
            the time an object gets updated
        """
        if len(kwargs) > 0:
            kwargs['created_at'] = datetime.fromisoformat(kwargs['created_at'])
            kwargs['updated_at'] = datetime.fromisoformat(kwargs['updated_at'])
            for key, value in kwargs.items():
                if key != "__class__":
                    self.__dict__[key] = value

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        storage.new(self)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the public instance attribute updated_at with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all
        keys/values of __dict__ of the instance"""
        real_create, real_update = self.created_at, self.updated_at

        self.created_at = self.created_at.isoformat()
        self.updated_at = self.updated_at.isoformat()
        my_dict = self.__dict__ | {"__class__": self.__class__.__name__}

        self.created_at, self.updated_at = real_create, real_update
        return my_dict
