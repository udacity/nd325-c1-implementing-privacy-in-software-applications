from typing import Dict
import re

EMAIL_REGEX = re.compile(r'\b\S+@\S+\.\S+\b')
NATIONAL_ID_REGEX = re.compile(r'\b\d{3}(-|\s)?\d{2}(-|\s)?\d{4}\b')
PHONE_NUMBER_REGEX = re.compile(r'((\b|\+)\d{1,3}|\d{,3})(-|\s)?\(?\d{3}\)?(-|\s)?\d{3}(-|\s)?\d{4}\b')


class RedactionValue:
    """
    An enum of mappings for different types of redactions
    """
    REDACTED_EMAIL = "[REDACTED EMAIL]"
    REDACTED_PHONE_NUMBER = "[REDACTED PHONE NUMBER]"
    REDACTED_NATIONAL_ID = "[REDACTED NATIONAL ID]"
    REDACTED_NAME = "[REDACTED NAME]"


def redact_free_text(free_text: str, overlap_keywords: Dict[str, RedactionValue]) -> str:
    """
    :param: free_text The free text to remove sensitive data from
    :returns: The redacted free text
    """
    # COMPLETED: Student should be adding in first and last name as parameters. In this solution, they're passed in as
    #            the parameter overlap_keywords

    redacted_text = re.sub(EMAIL_REGEX, RedactionValue.REDACTED_EMAIL, free_text)
    redacted_text = re.sub(NATIONAL_ID_REGEX, RedactionValue.REDACTED_NATIONAL_ID, redacted_text)
    redacted_text = re.sub(PHONE_NUMBER_REGEX, RedactionValue.REDACTED_PHONE_NUMBER, redacted_text)

    for keyword, replacement_value in overlap_keywords:
        redacted_text = redacted_text.replace(keyword, replacement_value)

    return redacted_text
