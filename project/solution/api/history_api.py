#
# This file contains the API for historical information
#

from solution.objects.voter import SensitiveVoter, ObfuscatedVoter


def get_voter_history(voter: SensitiveVoter):
    """
    Gets the history of the given voter.
    """
    obfuscated_voter: ObfuscatedVoter = voter.get_obfuscated_voter()
    raise NotImplementedError()


def delete_voter_history(voter: SensitiveVoter):
    """
    Deletes the history of the given voter.
    """
    obfuscated_voter: ObfuscatedVoter = voter.get_obfuscated_voter()
    raise NotImplementedError()


