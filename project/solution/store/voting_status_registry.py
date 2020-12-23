#
# This file contains an interface with the voting status registry, which contains the information
# for the status of voters in the election.
#

from solution.objects.voter import ObfuscatedVoter, VoterStatus


def mark_voter_as_having_voted(voter: ObfuscatedVoter):
    pass


def mark_voter_as_fraudulent(voter: ObfuscatedVoter):
    pass


def get_voter_status(voter: ObfuscatedVoter) -> VoterStatus:
    pass


class StoredVoterStatus(Base):
    __tablename__ = 'voter_status'
    obfuscated_voter_id = Column(String, primary_key=True)
    status = Column(String)

