from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///responses.db')
Session = sessionmaker(bind=engine)

class AIResponse(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    number = Column(String)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(engine)
