from .hash_dictionary import hash_file


def dictionary_cracking(hashes: list[str], dictionary: str) -> list[str]:
    """
    Crack hashed passwords using a dictionary file by comparing hashed dictionary entries to the target hashes.

    Args:
        hashes (list[str]): A list of hashed passwords to be cracked.
        dictionary (str): The path to the dictionary file containing potential plain text passwords.

    Returns:
        list[str]: A list of cracked plain text passwords corresponding to the input hashes.
    """
    plaintext_pass = [None] * len(hashes)
    hashed_file = hash_file(dictionary)
    for index, hash in enumerate(hashes):
        if hash in hashed_file:
            plaintext_pass[index] = hashed_file[hash]

    return plaintext_pass


def dictionary_cracking_with_salt(
    hashes: list[tuple[str, str]], dictionary: str
) -> list[str]:
    """
    Crack hashed passwords that use salts, by comparing hashed dictionary entries (with salt) to the target hashes.

    Args:
        hashes (list[tuple[str, str]]): A list of tuples where the first element is a hashed password and the second
        element is the salt.
        dictionary (str): The path to the dictionary file containing potential plain text passwords.

    Returns:
        list[str]: A list of cracked plain text passwords corresponding to the input hashes, taking into account
        the salt for each hash.
    """
    plaintext_pass = [None] * len(hashes)
    for index, hash in enumerate(hashes):
        hashed_file = hash_file(dictionary, hash[1])
        if hashes[index][0] in hashed_file:
            plaintext_pass[index] = hashed_file[hash[0]]

    return plaintext_pass
