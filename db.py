from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
	__tablename__ = "Users"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer)
	language = Column(String(2))

class MediaIds(Base):
	__tablename__ = "Media Ids"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer)
	user_name = Column(String(255))
	user_text = Column(String(255))
	msg_type = Column(String(255))
	

class Admin(Base):
	__tablename__ = "Admins"
	id = Column(Integer, primary_key=True)
	admin_id = Column(Integer)
	user_id = Column(Integer)
	user_name = Column(String(255))
	user_text = Column(String(255))
	msg_type = Column(String(255))


class Admin_g(Base):
	__tablename__ = 'Admins for group'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer)
	user_name = Column(String(255))