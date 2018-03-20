from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

## Initiate SQLite as the database engine and file location ##
engine = create_engine('sqlite:///CoinBull.db', echo=True)
Base = declarative_base()

class User(Base):
	"""
	Define user class with basic username and password
	"""
	__tablename__ = "users"

	## Define the data type for columns id, username, password ##
	id = Column(Integer, primary_key=True)
	username = Column(String)
	password = Column(String)

	def __init__(self, username, password):
		self.username = username
		self.password = password

## Publish changes to database ##
Base.metadata.create_all(engine)