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

    # TODO: Implement this method
    def get_obfuscated_voter(self) -> ObfuscatedVoter:
        """
        Converts this object (self) into its obfuscated version
        """
        raise NotImplementedError()


class VoterStatus:
    """
    An enum that represents the current status of a voter.
    """
    BALLOT_COUNTED = "ballot counted"
    FRAUD_COMMITTED = "fraud committed"
    NO_BALLOT_RECEIVED = "no ballot received"
