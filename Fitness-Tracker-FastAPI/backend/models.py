from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Fitness(Base):
    __tablename__ = "fitness"
    id = Column(Integer, primary_key=True)
    workout = Column(String)
    duration = Column(Integer)
    calories = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
