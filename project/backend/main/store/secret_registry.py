#
# Secrets themselves are sensitive, so we don't store them in our codebase. Instead, we store them as environment
# variables
#

import os


def get_secret(secret_name: str) -> str:
    """
    Gets a secret, if it exists. Otherwise, returns None
    """
    return os.getenv(secret_name)


def get_or_create_secret(secret_name: str, secret_value: str) -> str:
    """
    Will only create a secret if there isn't an existing secret. Will return the value of that secret.

    :param: secret_name The name of the secret, which can be used for future lookups
    :param: secret_value The secret value to store, if a secret does not currently exist 
    :return: The value of the secret with name secret_name
    """
    existing_secret = get_secret(secret_name)
    if existing_secret:
        return existing_secret

    overwrite_secret(secret_name, secret_value)
    return secret_value


def overwrite_secret(secret_name: str, secret_value):
    """
    Will overwrite the secret, even if there already is a secret present for the given secret_name
    """
    os.environ[secret_name] = secret_value

