#
# This file is the internal-only API that allows for the population of the voter registry.
# This API should not be exposed as a REST API for election security purposes.
#
from typing import List
from solution.objects.voter import SensitiveVoter, VoterStatus
from solution.objects.candidate import Candidate
from solution.store.data_registry import VotingStore

#
# Voter Registration
#


def register_voter(voter: SensitiveVoter):
    """
    Registers a specific voter for the election. This method doesn't verify that the voter is eligible to vote or any
    such legal logistics -- it simply registers them if they aren't currently registered.

    :param: voter The voter to register
    """
    # TODO: Implement this!
    raise NotImplementedError()


def get_voter_status(voter: SensitiveVoter) -> VoterStatus:
    """
    Checks to see if the specified voter is registered.

    :param: voter The voter to check the registration status of
    :returns: The status of the voter that best describes their situation
    """
    # TODO: Implement this!
    raise NotImplementedError()


def de_register_voter(voter: SensitiveVoter):
    """
    De-registers a voter from voting. This is to be used when the user requests to be removed from the system.
    """
    # TODO: Implement this!
    raise NotImplementedError()


#
# Candidate Registration
#

def register_candidate(candidate: Candidate):
    """
    Registers a candidate for the election, if not already registered.
    """
    store = VotingStore.get_instance()
    store.add_candidate(candidate)


def candidate_is_registered(candidate: Candidate) -> bool:
    """
    Checks to see if the specified candidate is registered.

    :param: candidate The candidate to check the registration status of
    :returns: Boolean TRUE if the candidate is registered. Boolean FALSE otherwise.
    """
    store = VotingStore.get_instance()
    return store.get_candidate(candidate.candidate_id) is not None


def get_all_candidates() -> List[Candidate]:
    store = VotingStore.get_instance()
    return store.get_all_candidates()
