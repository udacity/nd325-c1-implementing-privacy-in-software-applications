#
# Secrets themselves are sensitive, so we don't store them in our codebase. Instead, we store them as environment
# variables
#

import os
import bcrypt


def get_secret(secret_name: str) -> str:
    """
    Gets a secret, if it exists. Otherwise, returns None
    """
    return os.getenv(secret_name)


def overwrite_secret(secret_name: str, secret_value):
    """
    Will overwrite the secret, even if there already is a secret present for the given secret_name
    """
    os.environ[secret_name] = secret_value


def gen_salt() -> bytes:
    return bcrypt.gensalt(5)