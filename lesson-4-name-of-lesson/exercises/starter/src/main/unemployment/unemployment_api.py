from typing import Set

from src.main.unemployment.privacy import obfuscated_national_id, encrypt_email_address, decrypt_email_address
from src.main.unemployment.unemployment_store import UnemploymentStore


def mark_citizen_as_unemployed(sensitive_national_id: str, plaintext_email_address: str):
    """
    Marks the citizen with the corresponding sensitive national id as unemployed
    :param sensitive_national_id: A sensitive national ID
    :param plaintext_email_address: A plaintext email address corresponding to the unemployed citizen
    """
    UnemploymentStore.get_instance().mark_citizen_as_unemployed(
        obfuscated_national_id(sensitive_national_id), encrypt_email_address(plaintext_email_address))


def citizen_can_receive_unemployment(sensitive_national_id: str) -> bool:
    """
    Checks to see if the individual is both unemployed, and is not incarcerated.

    :param sensitive_national_id: A sensitive national ID
    :return: Boolean true if the citizen is unemployed. Boolean false otherwise
    """
    unemployment_store = UnemploymentStore.get_instance()
    return unemployment_store.verify_candidate_is_unemployed(obfuscated_national_id(sensitive_national_id)) and \
        not unemployment_store.verify_citizen_is_incarcerated(obfuscated_national_id(sensitive_national_id))


def unmark_citizen_as_unemployed(sensitive_national_id: str):
    """
    Unmarks the citizen with the corresponding sensitive national id as unemployed
    :param sensitive_national_id: A sensitive national ID
    """
    UnemploymentStore.get_instance() \
        .unmark_citizen_as_unemployed(obfuscated_national_id(sensitive_national_id))


def get_all_email_addresses() -> Set[str]:
    """
    Gets all the email addresses in the database in their plaintext form
    :return: A set of strings that represent the plaintext email addresses of all unemployed individuals
    """
    encrypted_email_addresses = UnemploymentStore.get_instance().get_all_email_addresses()
    return {decrypt_email_address(x) for x in encrypted_email_addresses}
