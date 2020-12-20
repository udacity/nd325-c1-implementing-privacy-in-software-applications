#
# This file contains an interface with the ballot registry, which is the complete database of ballots.
#

from solution.objects.voter import ObfuscatedVoter
from solution.objects.ballot import Ballot, BallotNumber


def issue_new_ballot(voter: ObfuscatedVoter) -> BallotNumber:
    """
    Stores and issues a new ballot, to a specific voter. A voter can receive multiple ballots,
    but only one will be counted.

    :param: voter The voter to whom this new ballot is to be issued to. Only this voter may return this ballot.
    :return: A ballot
    """
    # TODO: Implement this!
    pass


def invalidate_ballot(ballot_number: BallotNumber):
    """
    Marks a ballot as invalid so that it cannot be used again
    """
    # TODO(mpatil): Implement this!
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
