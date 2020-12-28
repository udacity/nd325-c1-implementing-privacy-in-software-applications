from typing import List

from backend.objects.voter import SensitiveVoter, BallotStatus
from backend.objects.candidate import Candidate
from backend.objects.ballot import Ballot


def issue_ballot(voter: SensitiveVoter) -> str:
    # TODO: Implement this!
    raise NotImplementedError()


def count_ballot(ballot: Ballot, voter: SensitiveVoter) -> BallotStatus:
    """
    Validates and counts the ballot for the given voter. If the ballot contains a sensitive comment, this method will
    appropriately redact the sensitive comment.

    This method will return the following upon the completion:
    1. BallotStatus.FRAUD_COMMITTED - If the voter has already voted
    2. BallotStatus.VOTER_BALLOT_MISMATCH - The ballot does not belong to this voter
    3. BallotStatus.INVALID_BALLOT - The ballot has been invalidated, or does not exist
    2. BallotStatus.NOT_REGISTERED - If the voter cannot be found in the voter registry
    3. BallotStatus.BALLOT_COUNTED - If the ballot submitted in this request was successfully counted

    :param: ballot The Ballot to count
    :returns: The Voter Status after the ballot has been processed.
    """
    # TODO: Implement this!
    raise NotImplementedError()


def invalidate_ballot(ballot_number: str) -> bool:
    """
    Marks a ballot as invalid so that it cannot be used. This should work on ballots that have been cast
    and ballots that have not been cast. Note that if a voter casts a ballot, and then it's invalidated, the voter is
    entitled to cast another ballot and have that be counted without being flagged for fraud.

    If the ballot does not exist, this method will return false.

    :returns: If the ballot does not exist, will return Boolean FALSE. Otherwise will return Boolean TRUE.
    """
    # TODO: Implement this!
    raise NotImplementedError()


def verify_ballot(voter: SensitiveVoter, ballot_number: str):
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
    raise NotImplementedError()


def get_all_ballot_comments() -> List[str]:
    """
    Returns a list of all the ballot comments that are non-empty.
    :returns: A list of all the ballot comments that are non-empty
    """
    # TODO: Implement this!
    raise NotImplementedError()


def compute_election_winner() -> Candidate:
    """
    Computes the winner of the election - the candidate that gets the most votes (even if there is not a majority).
    :return: The winning Candidate
    """
    # TODO: Implement this!
    raise NotImplementedError()
