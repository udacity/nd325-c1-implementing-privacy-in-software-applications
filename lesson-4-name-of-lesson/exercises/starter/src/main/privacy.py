
#
# Exercise 1
#

def obfuscated_national_id(sensitive_national_id: str) -> str:
    """
    Generates an obfuscated national identifier from a sensitive national identifier

    :param sensitive_national_id: The sensitive national ID of an individual
    :return: An obfuscated string that corresponds to the sensitive national id of an individual
    """
    # TODO: Implement this! If you need to use secrets, use the secret_registry.py file to maintain them.
    return sensitive_national_id  # Change this - obfuscate this in some way

#
# Exercise 2
#


def encrypt_email_address(plaintext_email_address: str) -> str:
    """
    Derives an obfuscated (encrypted) email address from a plaintext email address

    :param plaintext_email_address: The plaintext email address
    :return: An encrypted string that corresponds to the the email address of an individual
    """
    # TODO: Implement this! If you need to use secrets, use the secret_registry.py file to maintain them.
    return plaintext_email_address  # Change this - encrypt this


def decrypt_email_address(encrypted_email_address: str) -> str:
    """
    Derives an plaintext email address from an encrypted email address

    :param encrypted_email_address: The encrypted email address
    :return: The plaintext string that is the email address of a certain individual
    """
    # TODO: Implement this! If you need to use secrets, use the secret_registry.py file to maintain them.
    return encrypted_email_address  # Change this - decrypt this


#
# Exercise 3
#

def encrypt_incarceration_status(incarcerated: bool) -> str:
    """
    :param incarcerated: An encrypted value representing whether an individual was incarcerated or not
    :return: A human-readable boolean value indicating whether an individual was incarcerated or not.
    """
    # TODO: Implement this! If you need to use secrets, use the secret_registry.py file to maintain them.
    return str(incarcerated)  # Change this - encrypt this


def decrypt_incarceration_status(encrypted_incarcerated: str) -> bool:
    """
    :param encrypted_incarcerated: An encrypted value representing whether an individual was incarcerated or not
    :return: A human-readable boolean value indicating whether an individual was incarcerated or not.
    """
    # TODO: Implement this! If you need to use secrets, use the secret_registry.py file to maintain them.
    return encrypted_incarcerated != str(False)  # Change this - decrypt this

