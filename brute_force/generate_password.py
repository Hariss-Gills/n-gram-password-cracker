from .generate_lex_order import generate_lex_order_at_len
from string import ascii_lowercase, digits
import hashlib

CHARS = ascii_lowercase + digits


def brute_force_cracking(hashes: list[str]) -> list[str]:
    """
    Attempt to brute-force crack the provided hashes by generating all possible strings and hashing them.
    It tries to find the matching plain text password for each hash.

    Args:
        hashes (list[str]): A list of hashed values to be cracked.

    Returns:
        list[str]: A list of cracked plain text passwords corresponding to the input hashes.
    """

    plaintext_pass = [None] * len(hashes)
    shortlex_order = []
    length = 0

    while None in plaintext_pass:
        shortlex_order += generate_lex_order_at_len(CHARS, length)
        for string in shortlex_order:
            print(string)
            hashed_val = hashlib.sha512(string.encode()).hexdigest()
            if hashed_val in hashes:
                index_of_hashed_val = hashes.index(hashed_val)
                plaintext_pass[index_of_hashed_val] = string
                if None not in plaintext_pass:
                    break
        length += 1

    return plaintext_pass
