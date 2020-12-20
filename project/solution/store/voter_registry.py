#
# This file contains an interface with the voter registry, which is the complete database of voters.
#

from solution.objects.voter import ObfuscatedVoter


def add_voter(voter: ObfuscatedVoter):
    """
    Adds an individual voter into the voter registry.
    """
    # TODO(mpatil): Implement this!
    raise NotImplementedError()


def is_registered_voter(voter: ObfuscatedVoter) -> bool:
    """
    Checks if a voter is registered to vote.

    :return: Boolean True if the voter is a registered voter. Boolean False otherwise
    """
    # TODO(mpatil): Implement this!
    raise NotImplementedError()


def de_register_voter(voter: ObfuscatedVoter):
    """
    De-registers a voter from voting. This is to be used when the user requests to be removed from the system.
    """
    # TODO(mpatil): Implement this!
    raise NotImplementedError()
