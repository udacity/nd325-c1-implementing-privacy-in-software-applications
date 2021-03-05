from base64 import b64encode, b64decode

from secret_registry import get_secret_bytes, overwrite_secret_bytes
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import re, jsons


def encrypt_phone_number(plaintext_phone_number: str) -> str:
    sanitized_phone_number = re.sub(r"\s|\.|-|\(|\)|\+", "", plaintext_phone_number)
    expected_bytes = int(256 / 8)  # For 256-bit AES SIV

    encryption_key = get_secret_bytes("Phone Number Encryption Key")
    if not encryption_key:
        encryption_key = get_random_bytes(expected_bytes * 2)
        overwrite_secret_bytes("Phone Number Encryption Key", encryption_key)

    nonce = get_random_bytes(expected_bytes)
    cipher = AES.new(encryption_key, AES.MODE_SIV, nonce=nonce)
    cipher.update(b"")

    ciphertext, tag = cipher.encrypt_and_digest(sanitized_phone_number.encode("utf-8"))

    ciphertext_str = b64encode(ciphertext).decode("utf-8")
    tag_str = b64encode(tag).decode("utf-8")
    nonce_str = b64encode(nonce).decode("utf-8")

    return jsons.dumps({'ciphertext': ciphertext_str, 'tag': tag_str, 'nonce': nonce_str})

def decrypt_phone_number(encrypted_phone_number: str) -> str:
    metadata_strings = jsons.loads(encrypted_phone_number)
    ciphertext = b64decode(metadata_strings['ciphertext'].encode("utf-8"))
    tag = b64decode(metadata_strings['tag'].encode("utf-8"))
    nonce = b64decode(metadata_strings['nonce'].encode("utf-8"))

    encryption_key = get_secret_bytes("Phone Number Encryption Key")

    cipher = AES.new(encryption_key, AES.MODE_SIV, nonce=nonce)
    cipher.update(b"")

    return cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8")
