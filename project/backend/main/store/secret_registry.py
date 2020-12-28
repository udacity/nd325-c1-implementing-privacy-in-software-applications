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


def create_secret(secret_name: str, secret_value: str) -> bool:
    """
    Will only create a secret if there isn't an existing secret.

    :return: Boolean True if creation was successful. Boolean False otherwise
    """
    if get_secret(secret_name):
        return False

    overwrite_secret(secret_name, secret_value)
    return True


def overwrite_secret(secret_name: str, secret_value):
    """
    Will overwrite the secret, even if there already is a secret present for the given secret_name
    """
    os.environ[secret_name] = secret_value

