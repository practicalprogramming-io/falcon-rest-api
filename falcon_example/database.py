import datetime
from falcon_example import settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class Cars(Base):

    __tablename__ = 'cars'

    cars_id = Column(Integer, primary_key=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    color = Column(String)
    updated = Column(DateTime)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


engine = create_engine(URL(**settings.DATABASE))
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
