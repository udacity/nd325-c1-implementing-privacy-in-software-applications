from secret_registry import get_secret_bytes, overwrite_secret_bytes
import re, bcrypt


def hash_phone_number(phone_number: str) -> str:
    sanitized_phone_number = re.sub(r"\s|\.|-|\(|\)|\+", "", phone_number)
    pepper = get_secret_bytes("Phone Number Pepper")
    if not pepper:
        pepper = bcrypt.gensalt()
        overwrite_secret_bytes("Phone Number Pepper", pepper)

    return bcrypt.hashpw(sanitized_phone_number.encode("utf-8"), pepper).decode("utf-8")
