#!/usr/bin/python3
"""This is the state class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    
    if os.getenv('HBNB_TYPE_STORAGE') == 'file':
        @property
        def cities(self):
            obs = {}
            for k, v in models.storage.all(models.City).items():
                if v.state_id == self.id:
                    obs[k] = v
            return obs