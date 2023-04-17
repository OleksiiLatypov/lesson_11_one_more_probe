from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from connect_db import get_db, Base, engine
from sqlalchemy.orm import relationship


class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)


class Cat(Base):
    __tablename__ = 'cats'
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True)
    age = Column(Integer)
    vaccinated = Column(Boolean)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('owners.id'),
                      nullable=True)  # nullable means that cat may not have owner NULL

    owner = relationship(Owner, backref='cats')


Base.metadata.create_all(bind=engine)
