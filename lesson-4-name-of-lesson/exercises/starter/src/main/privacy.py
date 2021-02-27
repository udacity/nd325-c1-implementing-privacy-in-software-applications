
#
# Exercise 1
#
from base64 import b64encode, b64decode

import bcrypt
import jsons
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from src.main.secret_registry import get_secret_str, gen_salt_or_pepper, overwrite_secret_str, UTF_8, get_secret_bytes, \
    overwrite_secret_bytes


VOTER_MINIMIZATION_PEPPER = "VOTER_MINIMIZATION_PEPPER"
NAME_ENCRYPTION_KEY_AES_SIV = "NAME_ENCRYPTION_KEY_AES_SIV"
INCARCERATED_ENCRYPTION_KEY_AES_SIV = "INCARCERATED_ENCRYPTION_KEY_AES_SIV"


def obfuscated_national_id(sensitive_national_id: str) -> str:
    """
    Generates an obfuscated national identifier from a sensitive national identifier

    :param sensitive_national_id: The sensitive national ID of an individual
    :return: An obfuscated string that corresponds to the sensitive national id of an individual
    """
    pepper = get_secret_str(VOTER_MINIMIZATION_PEPPER)
    if not pepper:
        pepper = str(gen_salt_or_pepper(), UTF_8)
        overwrite_secret_str(VOTER_MINIMIZATION_PEPPER, pepper)

    return str(bcrypt.hashpw(sensitive_national_id.encode(UTF_8), pepper.encode(UTF_8)), UTF_8)

#
# Exercise 2
#


def encrypt_email_address(plaintext_email_address: str) -> str:
    """
    Derives an obfuscated (encrypted) email address from a plaintext email address

    :param plaintext_email_address: The plaintext email address
    :return: An encrypted string that corresponds to the the email address of an individual
    """
    expected_bytes = 32  # For AES SIV 256

    name_encryption_key = get_secret_bytes(NAME_ENCRYPTION_KEY_AES_SIV)
    if not name_encryption_key:
        name_encryption_key = get_random_bytes(expected_bytes * 2)
        overwrite_secret_bytes(NAME_ENCRYPTION_KEY_AES_SIV, name_encryption_key)

    cipher = AES.new(name_encryption_key, AES.MODE_SIV)

    cipher.update(b"")
    ciphertext, tag = cipher.encrypt_and_digest(plaintext_email_address.encode(UTF_8))

    json_v = [b64encode(x).decode(UTF_8) for x in (ciphertext, tag)]
    return jsons.dumps(dict(zip(['ciphertext', 'tag'], json_v)))


def decrypt_email_address(encrypted_email_address: str) -> str:
    """
    Derives an plaintext email address from an encrypted email address

    :param encrypted_email_address: The encrypted email address
    :return: The plaintext string that is the email address of a certain individual
    """
    name_encryption_key = get_secret_bytes(NAME_ENCRYPTION_KEY_AES_SIV)
    b64 = jsons.loads(encrypted_email_address)
    json_dict = {k: b64decode(b64[k]) for k in ['ciphertext', 'tag']}
    cipher = AES.new(name_encryption_key, AES.MODE_SIV)
    cipher.update(b"")
    return cipher.decrypt_and_verify(json_dict['ciphertext'], json_dict['tag']).decode(UTF_8)


#
# Exercise 3
#

def encrypt_incarceration_status(incarcerated: bool) -> str:
    """
    :param incarcerated: An encrypted value representing whether an individual was incarcerated or not
    :return: A human-readable boolean value indicating whether an individual was incarcerated or not.
    """
    expected_bytes = 32  # For AES SIV 256

    name_encryption_key = get_secret_bytes(INCARCERATED_ENCRYPTION_KEY_AES_SIV)
    if not name_encryption_key:
        name_encryption_key = get_random_bytes(expected_bytes * 2)
        overwrite_secret_bytes(INCARCERATED_ENCRYPTION_KEY_AES_SIV, name_encryption_key)

    nonce = get_random_bytes(expected_bytes)
    cipher = AES.new(name_encryption_key, AES.MODE_SIV, nonce=nonce)

    cipher.update(b"")
    ciphertext, tag = cipher.encrypt_and_digest(str(incarcerated).encode(UTF_8))

    json_v = [b64encode(x).decode(UTF_8) for x in (nonce, ciphertext, tag)]
    return jsons.dumps(dict(zip(['nonce', 'ciphertext', 'tag'], json_v)))


def decrypt_incarceration_status(encrypted_incarcerated: str) -> bool:
    """
    :param encrypted_incarcerated: An encrypted value representing whether an individual was incarcerated or not
    :return: A human-readable boolean value indicating whether an individual was incarcerated or not.
    """
    name_encryption_key = get_secret_bytes(INCARCERATED_ENCRYPTION_KEY_AES_SIV)
    b64 = jsons.loads(encrypted_incarcerated)
    json_dict = {k: b64decode(b64[k]) for k in ['nonce', 'ciphertext', 'tag']}
    cipher = AES.new(name_encryption_key, AES.MODE_SIV, nonce=json_dict['nonce'])
    cipher.update(b"")
    return cipher.decrypt_and_verify(json_dict['ciphertext'], json_dict['tag']).decode(UTF_8) != str(False)

