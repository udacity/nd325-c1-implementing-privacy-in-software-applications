#
# This file is the internal-only API that allows for the population of the voter registry.
# This API should not be exposed as a REST API for election security purposes.
#
from typing import List
from backend.main.objects.voter import Voter, VoterStatus
from backend.main.objects.candidate import Candidate
from backend.main.store.data_registry import VotingStore

#
# Voter Registration
#


def register_voter(voter: Voter) -> bool:
    """
    Registers a specific voter for the election. This method doesn't verify that the voter is eligible to vote or any
    such legal logistics -- it simply registers them if they aren't currently registered.

    :param: voter The voter to register. Note that the national ID for the voter might not come in a standard format -
            for example, "555-55-5555", "555555555" and "555 55 5555" should all be treated the same
    :returns: Boolean TRUE if the registration was successful. Boolean FALSE if the voter was already registered
              (based on their National ID)
    """
    # COMPLETED
    minimal_voter = voter.get_minimal_voter()
    store = VotingStore.get_instance()
    if store.get_voter_from_registry(minimal_voter.obfuscated_national_id) is not None:
        return False

    store.add_voter_to_registry(minimal_voter)
    return True


def get_voter_status(voter: Voter) -> VoterStatus:
    """
    Checks to see if the specified voter is registered.

    :param: voter The voter to check the registration status of. Note that the national ID for the voter might not come
            in a standard format - for example, "555-55-5555", "555555555" and "555 55 5555" should be treated the same
    :returns: The status of the voter that best describes their situation
    """
    # COMPLETED
    minimal_voter = voter.get_minimal_voter()
    store = VotingStore.get_instance()
    return store.get_voter_status(minimal_voter.obfuscated_national_id)


def de_register_voter(voter: Voter) -> bool:
    """
    De-registers a voter from voting. This is to be used when the user requests to be removed from the system.
    If a voter is a fraudulent voter, this should still be reflected in the system; they should not be able to
    de-registered.

    :param: voter The voter to de-register. Note that the national ID for the voter might not come in a standard format.
            For example, "555-55-5555", "555555555" and "555 55 5555" should be treated the same.
    :returns: Boolean TRUE if de-registration was successful. Boolean FALSE otherwise.
    """
    # COMPLETED
    minimal_voter = voter.get_minimal_voter()
    store = VotingStore.get_instance()
    if store.get_voter_from_registry(minimal_voter.obfuscated_national_id) is None:
        return False

    store.remove_voter_from_registry(minimal_voter.obfuscated_national_id)
    return True


#
# Candidate Registration (Already Implemented)
#

def register_candidate(candidate_name: str):
    """
    Registers a candidate for the election, if not already registered.
    """
    store = VotingStore.get_instance()
    store.add_candidate(candidate_name)


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
