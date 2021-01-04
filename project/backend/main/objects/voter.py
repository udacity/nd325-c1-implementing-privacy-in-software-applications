from backend.main.store.secret_registry import get_secret, overwrite_secret, gen_salt
import bcrypt

#
# This file contains classes that correspond to voters
#

from enum import Enum


def obfuscate_national_id(national_id: str) -> str:
    """
    Minimizes a national ID. The minimization may be either irreversible or reversible, but one might make life easier
    that the other, depending on the use-cases.

    :param: national_id A real national ID that is sensitive and needs to be obfuscated in some manner.
    :return: An obfuscated version of the national_id.
    """
    # COMPLETED: This is a sample implementation of this method that involves hashing. Using the bcrypt library to
    # guarantee slowness of hashing
    secret_name = "VOTER_MINIMIZATION_PEPPER"
    encoding_scheme = "utf-8"
    pepper = get_secret(secret_name)
    if not pepper:
        pepper = str(gen_salt(), encoding_scheme)
        overwrite_secret(secret_name, pepper)

    return str(
        bcrypt.hashpw(
            national_id.encode(encoding_scheme), pepper.encode(encoding_scheme)), encoding_scheme)


def obfuscate_name(name: str) -> str:
    """
    Minimizes a name. The minimization may be either irreversible or reversible, but one might make life easier
    that the other, depending on the use-cases.

    :param: name A plaintext name that is sensitive and needs to be obfuscated in some manner.
    :return: An obfuscated version of the name.
    """
    return name


class MinimalVoter:
    """
    Our representation of a voter, with the national id obfuscated (but still unique).
    This is the class that we want to be using in the majority of our codebase.
    """
    def __init__(self, obfuscated_first_name: str, obfuscated_last_name: str, obfuscated_national_id: str):
        self.obfuscated_national_id = obfuscated_national_id
        self.obfuscated_first_name = obfuscated_first_name
        self.obfuscated_last_name = obfuscated_last_name


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
        return MinimalVoter(
            obfuscate_name(self.first_name.strip()),
            obfuscate_name(self.last_name.strip()),
            obfuscate_national_id(self.national_id.replace("-", "").replace(" ", "").strip()))


class VoterStatus(Enum):
    """
    An enum that represents the current status of a voter.
    """
    NOT_REGISTERED = "not registered"
    REGISTERED_NOT_VOTED = "registered, but no ballot received"
    BALLOT_COUNTED = "ballot counted"
    FRAUD_COMMITTED = "fraud committed"


class BallotStatus(Enum):
    """
    An enum that represents the current status of a voter.
    """
    VOTER_BALLOT_MISMATCH = "the ballot doesn't belong to the voter specified"
    INVALID_BALLOT = "the ballot given is invalid"
    FRAUD_COMMITTED = "fraud committed: the voter has already voted"
    VOTER_NOT_REGISTERED = "voter not registered"
    BALLOT_COUNTED = "ballot counted"


