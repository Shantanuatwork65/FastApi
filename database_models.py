from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.ext.declarative import declarative_base

base=declarative_base()

class product(base):
    __tablename__ = "products"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String(255))
    description=Column(String(255))
    price=Column(Float)