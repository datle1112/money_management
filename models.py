from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __init__(self, name):
        self.name = name

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key = True)
    receiver = Column(String)
    date = Column(Date)
    amount = Column(Float)

    # Link to Category() object
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", backref="expenses")

    def __init__(self, receiver, date, amount):
        self.receiver = receiver
        self.date = date
        self.amount = amount