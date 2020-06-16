from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, TIMESTAMP, Sequence, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///chat.db", echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String)
    create_at: Column(TIMESTAMP)


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    sender_username = Column(String, ForeignKey('users.name'))
    receiver_username = Column(String, ForeignKey('users.name'))
    content_type = Column(String(20))
    content = Column(String(200))
    is_seen = Column(Boolean)
    create_at = Column(TIMESTAMP)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
