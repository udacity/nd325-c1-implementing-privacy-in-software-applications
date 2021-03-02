from typing import Optional

import pytest

from src.main.api import put_candidate, get_candidate, get_all_candidates, soft_delete_candidate, hard_delete_candidate, \
    candidate_data_subject_access_request
from src.main.hiring_store import HiringStore
import jsons

from exercises.starter.src.main.hiring_candidate import Candidate


class TestHiringStore:

    def test_put_and_get_candidate_basic(self):
        candidate1_name, candidate1_email = "Bob Jones", "bobjones@email.com"
        candidate2_name, candidate2_email = "Linda Vasquez", "lvasquez@email.com"

        candidate1_id = put_candidate(candidate1_name, candidate1_email)
        candidate2_id = put_candidate(candidate2_name, candidate2_email)

        assert get_candidate(candidate1_id).name == candidate1_name
        assert get_candidate(candidate1_id).email == candidate1_email

        assert get_candidate(candidate2_id).name == candidate2_name
        assert get_candidate(candidate2_id).email == candidate2_email

    def test_get_all_candidates_basic(self):
        candidate1_name, candidate1_email = "Bob Jones", "bobjones@email.com"
        candidate2_name, candidate2_email = "Linda Vasquez", "lvasquez@email.com"

        candidate1_id = put_candidate(candidate1_name, candidate1_email)
        candidate2_id = put_candidate(candidate2_name, candidate2_email)

        all_candidate_ids = [x.internal_id for x in get_all_candidates()]

        assert len(all_candidate_ids) == 2
        assert candidate1_id in all_candidate_ids
        assert candidate2_id in all_candidate_ids

    def test_soft_delete(self):
        candidate1_name, candidate1_email = "Bob Jones", "bobjones@email.com"
        candidate2_name, candidate2_email = "Linda Vasquez", "lvasquez@email.com"

        candidate1_id = put_candidate(candidate1_name, candidate1_email)
        candidate2_id = put_candidate(candidate2_name, candidate2_email)

        soft_delete_candidate(candidate1_id)

        # Make sure you can't get the candidate
        assert get_candidate(candidate1_id) is None

        # Make sure there's only one candidate in get all candidates
        all_candidate_ids = [x.internal_id for x in get_all_candidates()]

        assert len(all_candidate_ids) == 1
        assert candidate2_id in all_candidate_ids

    def test_hard_delete(self):
        candidate1_name, candidate1_email = "Bob Jones", "bobjones@email.com"
        candidate2_name, candidate2_email = "Linda Vasquez", "lvasquez@email.com"

        candidate1_id = put_candidate(candidate1_name, candidate1_email)
        candidate2_id = put_candidate(candidate2_name, candidate2_email)

        hard_delete_candidate(candidate1_id)

        # Make sure you can't get the candidate
        assert get_candidate(candidate1_id) is None

        # Make sure there's only one candidate in get all candidates
        all_candidate_ids = [x.internal_id for x in get_all_candidates()]

        assert len(all_candidate_ids) == 1
        assert candidate2_id in all_candidate_ids

    def test_data_subject_access_request(self):

        candidate1_name, candidate1_email = "Bob Jones", "bobjones@email.com"
        candidate1_id = put_candidate(candidate1_name, candidate1_email)

        # First, soft delete
        soft_delete_candidate(candidate1_id)

        # Make sure the output is a json string
        candidate1 = jsons.load(candidate_data_subject_access_request(candidate1_id), Optional[Candidate])

        # However, when a DSAR is triggered, we should be able to still get the candidate
        assert candidate1.name == candidate1_name

        # Then, hard delete
        hard_delete_candidate(candidate1_id)

        # When a DSAR is triggered, we should NOT be able to get the candidate
        assert candidate_data_subject_access_request(candidate1_id) is None

    @pytest.fixture(autouse=True)
    def clear_store_between_tests(self):
        HiringStore.refresh_instance()
