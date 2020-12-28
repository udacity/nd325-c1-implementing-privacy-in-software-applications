#
# This file contains classes that correspond to voters
#

class ObfuscatedVoter:
    """
    Our representation of a voter, with all sensitive information obfuscated (but still unique).
    This is the class that we want to be using in the majority of our codebase.
    """
    def __init__(self, obfuscated_national_id: str):
        self.obfuscated_national_id = obfuscated_national_id


class SensitiveVoter:
    """
    Our representation of a voter, including certain sensitive information.=
    This class should only be used in the initial stages when requests come in; in the rest of the
    codebase, we should be using the ObfuscatedVoter class
    """
    def __init__(self, national_id: str):
        self.national_id = national_id

    def get_obfuscated_voter(self) -> ObfuscatedVoter:
        """
        Converts this object (self) into its obfuscated version
        """
        # TODO: Implement this method
        raise NotImplementedError()


class VoterStatus:
    """
    An enum that represents the current status of a voter.
    """
    NOT_REGISTERED = "not registered"
    REGISTERED_NOT_VOTED = "registered, but no ballot received"
    BALLOT_COUNTED = "ballot counted"
    FRAUD_COMMITTED = "fraud committed"


class BallotStatus:
    """
    An enum that represents the current status of a voter.
    """
    VOTER_BALLOT_MISMATCH = "the ballot doesn't belong to the voter specified"
    INVALID_BALLOT = "the ballot given is invalid"
    FRAUD_COMMITTED = "fraud committed: the voter has already voted"
