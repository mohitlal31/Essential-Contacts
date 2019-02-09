import sys
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///itemCatalogWithUsers.db')
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    email = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)


class Category(Base):
    __tablename__ = 'category'

    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Person(Base):
    __tablename__ = 'person'

    name = Column(String, nullable=False)
    address = Column(String)
    mobile = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey(Category.id))
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'address': self.address,
            'mobile': self.mobile,
            'id': self.id,
            'category': self.category.name
        }


Base.metadata.create_all(engine)
