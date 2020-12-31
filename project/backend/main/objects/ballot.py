from backend.main.store.secret_registry import get_secret, overwrite_secret
import bcrypt
from time import time

ENCODING_SCHEME = "utf-8"
TIMESTAMP_SEPARATOR = "<--->"

class Ballot:
    """
    A ballot that exists in a specific, secret manner
    """
    def __init__(self, ballot_number: str, chosen_candidate_id: str, voter_comments: str):
        self.ballot_number = ballot_number
        self.chosen_candidate_id = chosen_candidate_id
        self.voter_comments = voter_comments


def generate_ballot_number(obfuscated_voter_id: str) -> str:

    # COMPLETED: Student should be taking a MinimalVoter, rather than a Voter, unless they have a good reason to take in
    #            a Voter. Also ok to take in the obfuscated_voter_id, as shown here. Uses the current time to achieve
    #            differentiation between ballot numbers.
    #
    #            A possible more elaborate solution is one where the student creates a table that maps obfuscated voter
    #            ids to salts, and looks up that salt for each obfuscated voter id. However, in this case a system
    #            pepper will still suffice.
    timestamp_millis_str = str(int(round(time() * 1000)))
    return generate_ballot_number_for_timestamp(obfuscated_voter_id, timestamp_millis_str)


def generate_ballot_number_for_timestamp(obfuscated_voter_id: str, timestamp_millis: str) -> str:

    secret_name = "BALLOT_NUMBER_GENERATION"
    pepper = get_secret(secret_name)
    if not pepper:
        pepper = str(bcrypt.gensalt(), ENCODING_SCHEME)
        overwrite_secret(secret_name, pepper)

    return str(
        bcrypt.hashpw(
            (obfuscated_voter_id + timestamp_millis).encode(ENCODING_SCHEME),
            pepper.encode(ENCODING_SCHEME)),
        ENCODING_SCHEME) + TIMESTAMP_SEPARATOR + timestamp_millis


def get_ballot_timestamp(ballot_number: str) -> str:
    timestamp_start_index = ballot_number.index(TIMESTAMP_SEPARATOR) + len(TIMESTAMP_SEPARATOR)
    return ballot_number[timestamp_start_index:]

