from typing import Set

from src.main.unemployment.unemployment_store import UnemploymentStore


def obfuscated_national_id(sensitive_national_id: str) -> str:
    """
    Generates an obfuscated national identifier from a sensitive national identifier

    :param sensitive_national_id: The sensitive national ID of an individual
    :return: An obfuscated string that corresponds to the sensitive national id of an individual
    """
    # TODO: Implement this! If you need to use secrets to make this happen, use the secret_registry.py file to maintain
    #       them.
    return sensitive_national_id  # Change this - obfuscate this in some way


def encrypt_email_address(plaintext_email_address: str) -> str:
    """
    Derives an obfuscated (encrypted) email address from a plaintext email address

    :param plaintext_email_address: The plaintext email address
    :return: An encrypted string that corresponds to the the email address of an individual
    """
    # TODO: Implement this! If you need to use secrets to make this happen, use the secret_registry.py file to maintain
    #       them.
    return plaintext_email_address  # Change this - encrypt this


def decrypt_email_address(encrypted_email_address: str) -> str:
    """
    Derives an plaintext email address from an encrypted email address

    :param encrypted_email_address: The encrypted email address
    :return: The plaintext string that is the email address of a certain individual
    """
    # TODO: Implement this! If you need to use secrets to make this happen, use the secret_registry.py file to maintain
    #       them.
    return encrypted_email_address  # Change this - decrypt this


def mark_citizen_as_unemployed(sensitive_national_id: str, plaintext_email_address: str):
    """
    Marks the citizen with the corresponding sensitive national id as unemployed
    :param sensitive_national_id: A sensitive national ID
    :param plaintext_email_address: A plaintext email address corresponding to the unemployed citizen
    """
    UnemploymentStore.get_instance().mark_citizen_as_unemployed(
        obfuscated_national_id(sensitive_national_id), encrypt_email_address(plaintext_email_address))


def is_citizen_unemployed(sensitive_national_id: str) -> bool:
    """
    :param sensitive_national_id: A sensitive national ID
    :return: Boolean true if the citizen is unemployed. Boolean false otherwise
    """
    return UnemploymentStore.get_instance() \
        .verify_candidate_is_unemployed(obfuscated_national_id(sensitive_national_id))


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
