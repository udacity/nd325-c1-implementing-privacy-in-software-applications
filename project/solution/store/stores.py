
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StoredVoter(Base):
    __tablename__ = 'voter'
    obfuscated_voter_id = Column(String, primary_key=True)
    status = Column(String)


class StoredBallot(Base):
    __tablename__ = 'ballot'
    ballot_number = Column(String, primary_key=True)
    status = Column(String)
