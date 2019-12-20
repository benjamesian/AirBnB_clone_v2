from sqlalchemy import create_engine
import os
from models.base_model import Base
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Create a DBStorage"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.getenv('HBNB_MYSQL_USER'),
                os.getenv('HBNB_MYSQL_PWD'),
                os.getenv('HBNB_MYSQL_HOST'),
                os.getenv('HBNB_MYSQL_DB')), pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        if cls:
            q = self.__session.query(cls).all()
            print(q)
        else:
            pass

    def reload(self):
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sess)
