from itertools import combinations_with_replacement
from typing import Set

REDACTED_PHONE_NUMBER = "[REDACTED PHONE NUMBER]"
REDACTED_ID_NUMBER = "[REDACTED ID NUMBER]"


def create_id_numbers_set() -> Set[str]:
    """
    Creates a set of ID numbers -- most of which follow a deterministic pattern, but some of which are complete outliers
    Additionally, not all of the numbers that follow a deterministic pattern are returned; some are removed before
    returning.

    This method simulates a database with a mostly consistent ID-ing scheme... with a few outliers, which sometimes
    happens in legacy databases.
    """
    special_id_numbers = {"111111", "122211", "112211", "122515532", "12553221", "125645331", "242352356", "87543733"}
    combinations = set(combinations_with_replacement([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 3))
    id_numbers = { str((100 * x[0] + 10 * x[1] + x[2]) * 100 + x[0] + x[1] + x[2]) for x in combinations}
    id_numbers = {'0' * (5 - len(x)) + x for x in id_numbers}
    for unwanted_number in ['11204', '11305', '11406', '11507']:
        id_numbers.remove(unwanted_number)
    return id_numbers.union(special_id_numbers)


def redact_phone_numbers(free_text: str) -> str:
    """
    Removes all phone numbers from the given free text, and returns the redacted format. For example, if the text is:
    >>> text = "Please contact me at (503) 289-2342"
    >>> redacted_text = redact_phone_numbers(text)
    >>> print(redacted_text)
    "Please contact me at [REDACTED PHONE NUMBER]"
    """
    # TODO: Implement this!
    raise NotImplementedError()


def redact_id_numbers(free_text: str) -> str:
    """
    Removes all names using overlap detection
    >>> text = "My ID Number is 13206"
    >>> redacted_text = redact_id_numbers(text)
    >>> print(redacted_text)
    "My ID Number if [REDACTED ID NUMBER]"
    """
    all_possible_id_numbers = create_id_numbers_set()
    # TODO: Implement this!
    raise NotImplementedError()
