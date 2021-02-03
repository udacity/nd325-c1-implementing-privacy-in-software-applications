from typing import List, Optional

from src.main.hiring_candidate import Candidate
from src.main.hiring_store import HiringStore


def put_candidate(candidate_name: str, candidate_email: str) -> int:
    """
    Put candidate data to hire into the store.
    """
    store = HiringStore.get_instance()
    return store.add_candidate(candidate_name, candidate_email)


def get_candidate(candidate_id: int) -> Optional[Candidate]:
    """
    If a candidate has been soft-deleted, the candidate should NOT show up here.
    """
    store = HiringStore.get_instance()
    return store.get_candidate(candidate_id)


def get_all_candidates() -> List[Candidate]:
    """
    Used to show all the candidates in a frontend. If a candidate has been soft-deleted, the candidate should NOT show
    up here.
    """
    store = HiringStore.get_instance()
    return store.get_all_candidates()

#
# Privacy APIs
#


def soft_delete_candidate(candidate_id: int):
    """
    Makes the data inaccessible, except for the `get_candidate_data` endpoint.
    """
    store = HiringStore.get_instance()
    return store.soft_delete_candidate(candidate_id)


def hard_delete_candidate(candidate_id: int):
    """
    Completely removes the candidate from the application-layer.
    """
    store = HiringStore.get_instance()
    return store.hard_delete_candidate(candidate_id)


def candidate_data_subject_access_request(candidate_id: int) -> Optional[Candidate]:
    """
    Used for data subject access requests. If a candidate has been soft-deleted, the candidate should NOT show up here.
    """
    store = HiringStore.get_instance()
    return store.candidate_data_subject_access_request(candidate_id)
