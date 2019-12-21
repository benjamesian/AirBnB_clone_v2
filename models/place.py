#!/usr/bin/python3
"""This is the place class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import (Table, MetaData,
                        Column, String, Integer, Float, ForeignKey)
from sqlalchemy.orm import relationship
import os


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             nullable=False, primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             nullable=False, primary_key=True))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, default=0.0, nullable=False)
    longitude = Column(Float, default=0.0, nullable=False)
    amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref='places',
                               cascade='all, delete-orphan')

        amenities = relationship('Amenity', secondary='place_amenity',
                                 back_populates='places', viewonly=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'file':
        @property
        def reviews(self):
            obs = {}
            for k, v in models.storage.all(models.Review).items():
                if v.state_id == self.id:
                    obs[k] = v
            return obs

        @property
        def amenities(self):
            obs = {}
            for k, v in models.storage.all(models.Amenity).items():
                if v.id in self.amenity_ids:
                    obs[k] = v
            return obs

        @amenities.setter
        def amenities(self, value):
            if not isinstance(value, models.Amenity):
                return
            self.amenity_ids.append(value.id)
