
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StoredVoter(Base):
    __tablename__ = 'voter'
    obfuscated_voter_id = Column(String, primary_key=True)

    # First and Last names are necessary for fraud enforcement
    first_name = Column(String)
    last_name = Column(String)
    status = Column(String)


class StoredBallot(Base):
    __tablename__ = 'ballot'
    ballot_number = Column(String, primary_key=True)
    chosen_candidate_id = Column(Integer, ForeignKey('candidate.candidate_id'))
    status = Column(String)


class StoredCandidate(Base):
    __tablename__ = 'candidate'
    candidate_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_name = Column(String)
