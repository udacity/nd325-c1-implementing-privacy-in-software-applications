from backend.main.store.secret_registry import get_secret, overwrite_secret
import bcrypt

#
# This file contains classes that correspond to voters
#

class MinimalVoter:
    """
    Our representation of a voter, with the national id obfuscated (but still unique).
    This is the class that we want to be using in the majority of our codebase.
    """
    def __init__(self, first_name: str, last_name: str, obfuscated_national_id: str):
        self.obfuscated_national_id = obfuscated_national_id
        self.first_name = first_name
        self.last_name = last_name


class Voter:
    """
    Our representation of a voter, including certain sensitive information.=
    This class should only be used in the initial stages when requests come in; in the rest of the
    codebase, we should be using the ObfuscatedVoter class
    """
    def __init__(self, first_name: str, last_name: str, national_id: str):
        self.national_id = national_id
        self.first_name = first_name
        self.last_name = last_name

    def get_minimal_voter(self) -> MinimalVoter:
        """
        Converts this object (self) into its obfuscated version
        """
        # This is a sample implementation of this method that involves hashing. Using the bcrypt library to guarantee
        # slowness of hashing
        secret_name = "VOTER_MINIMIZATION_PEPPER"
        encoding_scheme = "utf-8"
        pepper = get_secret(secret_name)
        if not pepper:
            pepper = str(bcrypt.gensalt(12), encoding_scheme)
            overwrite_secret(secret_name, pepper)

        obfuscated_national_id = str(
            bcrypt.hashpw(self.national_id.encode(encoding_scheme), pepper.encode(encoding_scheme)), encoding_scheme)
        return MinimalVoter(self.first_name, self.last_name, obfuscated_national_id)


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
    VOTER_NOT_REGISTERED = "voter not registered"
    BALLOT_COUNTED = "ballot counted"


