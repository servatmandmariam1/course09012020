from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date, ForeignKey, ForeignKeyConstraint, ARRAY, JSON
from dao.entities import *

Base = declarative_base()
class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key= True)
    username = Column(String(15), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(80))

class Dish(Base):
    __tablename__ = 'dish'
    dishname = Column(String(80), primary_key=True)
    calories_amount = Column(Integer, nullable=False)
    ingridients = Column(String, nullable=False)
    author = Column(String, nullable=False)
    type = Column(String, nullable=False)
    receipt = Column(String, nullable= False)
class Type(Base):
    __tablename__ = 'type'
    typename = Column(String(80), primary_key=True)


class Receipt(Base):
    __tablename__ = 'receipt'
    dishname_fk = Column(String(100), ForeignKey('dish.dishname'))
    receipt_content = Column(String(100), primary_key=True)


class Ingridient(Base):
    __tablename__ = 'ingridient'
    ingridient = Column(String(80), primary_key=True)


class Dish_Type(Base):
    __tablename__ = 'dish_type'
    dishname = Column(String(255), ForeignKey('Dish.dishname'), primary_key=True)
    type = Column(String(255), primary_key=True)

class Restaurant(Base):
    __tablename__ = 'restaurant'
    address = Column(String(80))
    city = Column(String(80))
    star = Column(Integer, nullable=False)
    country = Column(String(80))
    name = Column(String, primary_key=True)
    dishname_fk = Column(String(80))




    dishname_fk = Column(String(100), ForeignKey('dish.dishname'))