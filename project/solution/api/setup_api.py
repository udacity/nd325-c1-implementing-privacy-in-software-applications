#
# This file is the internal-only API that allows for the population of the voter registry.
# This API should not be exposed as a REST API for election security purposes.
#


from solution.objects.voter import SensitiveVoter
from solution.objects.candidate import Candidate


def register_voter(voter: SensitiveVoter):
    """
    Registers a specific voter for the election. This method doesn't verify that the voter is eligible to vote or any
    such legal logistics -- it simply registers them if they aren't currently registered.

    :param: voter The voter to register
    """
    raise NotImplementedError()


def voter_is_registered(voter: SensitiveVoter) -> bool:
    """
    Checks to see if the specified voter is registered.

    :param: voter The voter to check the registration status of
    :returns: Boolean TRUE if the voter is registered. Boolean FALSE otherwise.
    """
    raise NotImplementedError()


def register_candidate(candidate: Candidate):
    """
    Registers a candidate for the election, if not already registered.
    """
    raise NotImplementedError()


def candidate_is_registered(candidate: Candidate) -> bool:
    """
    Checks to see if the specified candidate is registered.

    :param: candidate The candidate to check the registration status of
    :returns: Boolean TRUE if the candidate is registered. Boolean FALSE otherwise.
    """
    raise NotImplementedError()
