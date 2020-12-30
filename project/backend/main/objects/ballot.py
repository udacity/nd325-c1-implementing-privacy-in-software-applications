from backend.main.store.secret_registry import get_secret, overwrite_secret
import bcrypt
from time import time


class Ballot:
    """
    A ballot that exists in a specific, secret manner
    """
    def __init__(self, ballot_number: str, chosen_candidate_id: str, voter_comments: str):
        self.ballot_number = ballot_number
        self.chosen_candidate_id = chosen_candidate_id
        self.voter_comments = voter_comments
        raise NotImplementedError()


def generate_ballot_number(obfuscated_voter_id: str) -> str:

    # COMPLETED: Student should be taking a MinimalVoter, rather than a Voter, unless they have a good reason to take in
    #            a Voter. Also ok to take in the obfuscated_voter_id, as shown here. Uses the current time to achieve
    #            differentiation between ballot numbers.
    #
    #            A possible more elaborate solution is one where the student creates a table that maps obfuscated voter
    #            ids to salts, and looks up that salt for each obfuscated voter id. However, in this case a system
    #            pepper will still suffice.

    secret_name = "BALLOT_NUMBER_GENERATION"
    encoding_scheme = "utf-8"
    pepper = get_secret(secret_name)
    if not pepper:
        pepper = str(bcrypt.gensalt(12), encoding_scheme)
        overwrite_secret(secret_name, pepper)

    timestamp_millis_str = str(int(round(time() * 1000)))

    return str(
        bcrypt.hashpw(
            (obfuscated_voter_id + timestamp_millis_str).encode(encoding_scheme),
            pepper.encode(encoding_scheme)),
        encoding_scheme)
