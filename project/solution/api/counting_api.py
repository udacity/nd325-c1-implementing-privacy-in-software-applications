from solution.objects.voter import SensitiveVoter, VoterStatus, ObfuscatedVoter
from solution.objects.candidate import Candidate
from solution.objects.ballot import BallotNumber, Ballot


def issue_ballot(voter: SensitiveVoter) -> BallotNumber:
    raise NotImplementedError()


def count_ballot(ballot: Ballot, voter: SensitiveVoter) -> bool:
    """
    :param: ballot The Ballot to count

    :returns: Whether or not the ballot was actually counted or not
    """

    # TODO: Verify that the ballot actually corresponds to the sensitive voter.
    # If it doesn't we should return false

    # TODO: Count the Ballot
    # TODO: Record that the Ballot

    raise NotImplementedError()


def invalidate_ballot(ballot_number: BallotNumber):
    """
    Marks a ballot as invalid so that it cannot be used again
    """
    # TODO: Implement this!
    pass


def verify_ballot(voter: ObfuscatedVoter, ballot_number: BallotNumber):
    """
    Verifies the following:

    1. That the ballot was specifically issued to the voter specified
    2. That the ballot is not invalid

    If all of the points above are true, then returns Boolean True. Otherwise returns Boolean False.

    :param: voter The voter about to cast the ballot with the given ballot number
    :param: ballot_number The ballot number of the ballot that is about to be cast by the given voter
    :returns: Boolean True if the ballot was issued to the voter specified, and if the ballot has not been marked as
              invalid. Boolean False otherwise.
    """
    # TODO: Implement this!
    pass


def compute_election_winner() -> Candidate:
    """
    :return: The winning Candidate
    """
    raise NotImplementedError()
