import pytest

from src.main.unemployment_api import mark_citizen_as_unemployed, citizen_can_receive_unemployment, unmark_citizen_as_unemployed, get_all_email_addresses
from src.main.unemployment_store import UnemploymentStore


class TestApi:
    def test_non_incarcerated_citizens_can_receive_benefits_if_unemployed(self):
        assert citizen_can_receive_unemployment("111-11-1111")
        assert citizen_can_receive_unemployment("222-22-2222")
        assert citizen_can_receive_unemployment("333-33-3333")
        assert citizen_can_receive_unemployment("444-44-4444")
        assert citizen_can_receive_unemployment("555-55-5555")

        assert not citizen_can_receive_unemployment("666-66-6666")
        assert not citizen_can_receive_unemployment("777-77-7777")
        assert not citizen_can_receive_unemployment("888-88-8888")

    def test_unmarking_for_unemployment(self):
        assert citizen_can_receive_unemployment("111-11-1111")
        unmark_citizen_as_unemployed("111-11-1111")
        assert not citizen_can_receive_unemployment("111-11-1111")

    def test_incarcerated_individuals_cannot_receive_unemployment(self):
        mark_citizen_as_unemployed("999-99-9999", "person@email.com", True)
        assert not citizen_can_receive_unemployment("999-99-9999")

    def test_get_all_emails(self):
        assert get_all_email_addresses() == \
               {"aadams@email.com", "bberg@email.com", "cchu@email.com", "ddeshpande@email.com", "eengland@email.com"}

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """
        Sets up the candidates and voters
        """
        UnemploymentStore.refresh_instance()

        # Populate unemployment registry
        mark_citizen_as_unemployed("111-11-1111", "aadams@email.com", False)
        mark_citizen_as_unemployed("222-22-2222", "bberg@email.com", False)
        mark_citizen_as_unemployed("333-33-3333", "cchu@email.com", False)
        mark_citizen_as_unemployed("444-44-4444", "ddeshpande@email.com", False)
        mark_citizen_as_unemployed("555-55-5555", "eengland@email.com", False)
        yield
