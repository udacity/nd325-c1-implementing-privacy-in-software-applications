from solution.objects.voter import SensitiveVoter, VoterStatus, ObfuscatedVoter
from solution.objects.candidate import Candidate
from solution.objects.ballot import Ballot


def issue_ballot(voter: SensitiveVoter) -> Ballot:
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


def compute_election_winner() -> Candidate:
    """
    :return: The winning Candidate
    """
    raise NotImplementedError()


def get_voter_status(voter: SensitiveVoter) -> VoterStatus:
    """
    Gets the status of the voter specified,

    :returns: a VoterStatus object corresponding to the given sensitive voter
    """
    obfuscated_voter: ObfuscatedVoter = voter.get_obfuscated_voter()
    raise NotImplementedError()
