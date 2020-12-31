from typing import Set, Optional

from backend.main.objects.voter import Voter, BallotStatus, VoterStatus
from backend.main.objects.candidate import Candidate
from backend.main.objects.ballot import Ballot
from backend.main.store.data_registry import VotingStore
from backend.main.objects.ballot import generate_ballot_number, get_ballot_timestamp,\
    generate_ballot_number_for_timestamp
from backend.main.detection.pii_detection import redact_free_text, RedactionValue


def issue_ballot(voter: Voter) -> Optional[str]:
    """
    Issues a new ballot to a given voter. The ballot number of the new ballot. This method should NOT invalidate any old
    ballots. If the voter isn't registered, should return None.

    :params: voter The voter to issue a new ballot to. Note that the national ID for the voter might not come in a
             standard format. For example, "555-55-5555", "555555555" and "555 55 5555" should be treated the same.
    :returns: The ballot number of the new ballot, or None if the voter isn't registered
    """
    store = VotingStore.get_instance()
    minimal_voter = voter.get_minimal_voter()

    if store.get_voter_status(minimal_voter.obfuscated_national_id) == VoterStatus.NOT_REGISTERED:
        return None
    else:
        new_ballot_number = generate_ballot_number(minimal_voter.obfuscated_national_id)
        store.issue_ballot(new_ballot_number)
        return new_ballot_number


def count_ballot(ballot: Ballot, voter: Voter) -> BallotStatus:
    """
    Validates and counts the ballot for the given voter. If the ballot contains a sensitive comment, this method will
    appropriately redact the sensitive comment.

    This method will return the following upon the completion:
    1. BallotStatus.FRAUD_COMMITTED - If the voter has already voted
    2. BallotStatus.VOTER_BALLOT_MISMATCH - The ballot does not belong to this voter (or if the voter isn't registered)
    3. BallotStatus.INVALID_BALLOT - The ballot has been invalidated, or does not exist
    4. BallotStatus.BALLOT_COUNTED - If the ballot submitted in this request was successfully counted

    :param: ballot The Ballot to count
    :param: voter The voter who the ballot corresponds to. Note that the national ID for the voter might not come in a
            standard format. For example, "555-55-5555", "555555555" and "555 55 5555" should be treated the same.
    :returns: The Ballot Status after the ballot has been processed.
    """
    store = VotingStore.get_instance()
    minimal_voter = voter.get_minimal_voter()

    sanitized_ballot = Ballot(ballot.ballot_number, ballot.chosen_candidate_id, redact_free_text(
        ballot.voter_comments, {
            minimal_voter.first_name: RedactionValue.REDACTED_NAME,
            minimal_voter.last_name: RedactionValue.REDACTED_NAME
        }))

    if not store.ballot_exists(ballot.ballot_number):
        return BallotStatus.INVALID_BALLOT
    elif not verify_ballot(voter, ballot.ballot_number):
        return BallotStatus.VOTER_BALLOT_MISMATCH

    return store.cast_ballot(minimal_voter.obfuscated_national_id, sanitized_ballot)


def invalidate_ballot(ballot_number: str) -> bool:
    """
    Marks a ballot as invalid so that it cannot be used. This should only work on ballots that have NOT been cast. If a
    ballot has already been cast, it cannot be invalidated.

    If the ballot does not exist or has already been cast, this method will return false.

    :returns: If the ballot does not exist or has already been cast, will return Boolean FALSE.
              Otherwise will return Boolean TRUE.
    """
    store = VotingStore.get_instance()
    if not store.ballot_exists(ballot_number) or store.ballot_has_been_cast(ballot_number):
        return False

    store.invalidate_ballot(ballot_number)
    return True


def verify_ballot(voter: Voter, ballot_number: str) -> bool:
    """
    Verifies the following:

    1. That the ballot was specifically issued to the voter specified
    2. That the ballot is not invalid

    If all of the points above are true, then returns Boolean True. Otherwise returns Boolean False.

    :param: voter The voter about to cast the ballot with the given ballot number
    :param: ballot_number The ballot number of the ballot that is about to be cast by the given voter
    :returns: Boolean True if the ballot was issued to the voter specified, and if the ballot has not been marked as
              invalid. Boolean False otherwise.
    """
    store = VotingStore.get_instance()
    if not store.ballot_exists(ballot_number):
        return False

    minimal_voter = voter.get_minimal_voter()
    ballot_timestamp = get_ballot_timestamp(ballot_number)
    result = ballot_number == generate_ballot_number_for_timestamp(minimal_voter.obfuscated_national_id, ballot_timestamp)
    return result


def get_all_ballot_comments() -> Set[str]:
    """
    Returns a list of all the ballot comments that are non-empty.
    :returns: A list of all the ballot comments that are non-empty
    """
    store = VotingStore.get_instance()
    return store.get_all_comments()


def compute_election_winner() -> Candidate:
    """
    Computes the winner of the election - the candidate that gets the most votes (even if there is not a majority).
    :return: The winning Candidate
    """
    # TODO: Implement this!
    raise NotImplementedError()


def get_all_fraudulent_voters() -> Set[str]:
    """
    Returns a complete list of voters who committed fraud. For example, if the following committed fraud:

    1. first: "John", last: "Smith"
    2. first: "Linda", last: "Navarro"

    Then this method would return {"John Smith", "Linda Navarro"} - with a space separating the first and last names.
    """
    # TODO: Implement this!
    raise NotImplementedError()
