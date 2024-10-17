from string import ascii_lowercase, digits
from itertools import product
from markov.generate_password import cracking_with_markov_chains
import hashlib
import json
import time
import pickle

CHARS = ascii_lowercase + digits


# Maybe use generator here to save memory
def generate_lex_order_at_len(alphabet: str, length: int) -> list[str]:
    """
    Generate all possible strings of a given length in lexicographical order using
    characters from the specified alphabet.

    Args:
        alphabet (str): The characters to use for generating combinations.
        length (int): The length of the generated strings.

    Returns:
        list[str]: A list of all possible strings of the specified length in lexicographical order.
    """

    lex_order_at_len = []
    # Use cartiesian product to find every combination at certain length
    # https://en.wikipedia.org/wiki/Lexicographic_order#Cartesian_products
    for combination in product(alphabet, repeat=length):
        lex_order_at_len.append("".join(combination))

    return lex_order_at_len


# Maybe do an early return
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
            hashed_val = hashlib.sha512(string.encode()).hexdigest()
            if hashed_val in hashes:
                index_of_hashed_val = hashes.index(hashed_val)
                plaintext_pass[index_of_hashed_val] = string
        length += 1

    return plaintext_pass


# Maybe add a way to proccess hashes in chunks
def hash_file(file_path: str, salt: str = "") -> dict[str, str]:
    """
    Hash all passwords in a file with an optional salt, returning a dictionary of hashed passwords.

    Args:
        file_path (str): The path to the file containing passwords (one per line).
        salt (str, optional): An optional salt to append to each password before hashing. Defaults to "".

    Returns:
        dict[str, str]: A dictionary where the keys are the hashed passwords and the values are the plain text passwords.
    """
    hashed_file = {}
    with open(file_path) as file:
        for password in file:
            clean_pass = password.strip()
            hashed_val = hashlib.sha512(f"{clean_pass}{salt}".encode()).hexdigest()
            hashed_file[hashed_val] = clean_pass

    return hashed_file


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


if __name__ == "__main__":
    with open("hashes.json") as json_file:
        data = json.load(json_file)

    start_time = time.time()
    task1_values = brute_force_cracking(data["task1_hashed_vals"])
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task1_values)

    start_time = time.time()
    task2_values = dictionary_cracking(
        data["task2_hashed_vals"], "password-data/PasswordDictionary.txt"
    )
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task2_values)

    # Python annotingly has no built in way to store tuples from json
    # https://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json
    task3_hashed_vals = data["task3_hashed_vals"]
    for index, item in enumerate(task3_hashed_vals):
        task3_hashed_vals[index] = tuple(item)

    start_time = time.time()
    task3_values = dictionary_cracking_with_salt(
        data["task3_hashed_vals"], "password-data/PasswordDictionary.txt"
    )
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task3_values)

    max_ngrams = 3
    with open(f"password-data/upto-{max_ngrams}-gram.pickle", "rb") as file:
        markov_chain = pickle.load(file)

    start_time = time.time()
    task4_values = cracking_with_markov_chains(data["task4_hashed_vals"], markov_chain)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task4_values)
