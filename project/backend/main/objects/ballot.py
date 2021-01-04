from backend.main.store.secret_registry import get_secret_str, overwrite_secret_str, gen_salt, UTF_8
import bcrypt
from time import time

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
    """
    Produces a ballot number. Feel free to add parameters to this method, if you feel those are necessary.

    Remember that ballot numbers must respect the following conditions:

    1. Voters can be issued multiple ballots. This can be because a voter might make a mistake when filling out one
       ballot, and therefore might need an additional ballot. However it's important that only one ballot per voter is
       counted.
    2. All ballots must be secret. Voters have the right to cast secret ballots, which means that it should be
       technically impossible for someone holding a ballot to associate that ballot with the voter.
    3. In order to minimize the risk of fraud, a nefarious actor should not be able to tell that two different ballots
       are associated with the same voter.

    :return: A string representing a ballot number that satisfies the conditions above
    """

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
    """
    Will deterministically produce a ballot number for a given obfuscated_voter_id and timestamp in milliseconds.

    This method works by appending the timestamp string to the end of the ballot, so it can be extracted in
    get_ballot_timestamp
    """
    secret_name = "BALLOT_NUMBER_GENERATION"
    pepper = get_secret_str(secret_name)
    if not pepper:
        pepper = str(gen_salt(), UTF_8)
        overwrite_secret_str(secret_name, pepper)

    return str(
        bcrypt.hashpw(
            (obfuscated_voter_id + timestamp_millis).encode(UTF_8),
            pepper.encode(UTF_8)),
        UTF_8) + TIMESTAMP_SEPARATOR + timestamp_millis


def get_ballot_timestamp(ballot_number: str) -> str:
    """
    Gets the timestamp when the ballot was created, based on the ballot_number.
    """
    timestamp_start_index = ballot_number.index(TIMESTAMP_SEPARATOR) + len(TIMESTAMP_SEPARATOR)
    return ballot_number[timestamp_start_index:]
