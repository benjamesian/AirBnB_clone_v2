#!/usr/bin/python3
""" New engine DBStorage for HBNB"""
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """Storage with SQL backend"""
    __engine = None
    __session = None

    def __init__(self):
        """Create an instance of DBStorage"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.getenv('HBNB_MYSQL_USER'),
                os.getenv('HBNB_MYSQL_PWD'),
                os.getenv('HBNB_MYSQL_HOST'),
                os.getenv('HBNB_MYSQL_DB')), pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of object in __session
        Args:
            cls: given class
        """
        if cls:
            if isinstance(cls, str):
                d = {
                    'user' : User,
                    'state': State,
                    'city' : City,
                    'place': Place,
                    'review': Review
                }
                cls = d.get(cls.lower())
            return self.__session.query(cls).all()
        out = []
        for model in (User, State, City, Place, Review):
            out += self.__session.query(model).all()
        return out

    def new(self, obj):
        """Adds the object to the current database session
        Args:
            obj: given object
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None
        Args:
            obj: given object
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload instances from db"""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sess)

    def close(self):
        """Close connection to storage."""
        self.__session.remove()
