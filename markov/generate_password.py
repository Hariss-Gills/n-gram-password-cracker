from .train_chain import LEFT_DELIM, RIGHT_DELIM, MarkovChain
import pickle
import random
import json
import time
import hashlib

MAX_PASSWORD_LENGTH = 100
MAX_UNIQUE_PASSWORDS = 1000000


def gen_character(markov_chain: MarkovChain, ngram: str) -> str:
    """
    Generate the next character based on the given n-gram and Markov chain.

    Looks up the next character in the Markov chain using
    the provided n-gram. If the n-gram is not found in the chain, it recursively
    shortens the n-gram and tries again.

    Args:
        markov_chain (MarkovChain): A MarkovChain object containing transition probabilities.
        ngram (str): The current sequence of characters (n-gram) to base the next character prediction on.

    Returns:
        str: The next predicted character.
    """
    if ngram in markov_chain:
        char = random.choices(
            list(markov_chain[ngram].keys()), weights=markov_chain[ngram].values()
        )[0]
        return char

    else:
        return gen_character(markov_chain, ngram[0:-1])


def generate_password(markov_chain: MarkovChain, ngram_length: int) -> str:
    """
    Generate a password based on the provided Markov chain model.

    Generates a password by starting with a delimiter and
    iteratively appending characters predicted by the Markov chain model
    until the right delimiter is reached or the maximum password length is
    exceeded.

    Args:
        markov_chain (MarkovChain): A MarkovChain object that represents the model.
        ngram_length (int): The length of the n-grams to consider when generating the password.

    Returns:
        str: The generated password, without the delimiters.
    """
    password = LEFT_DELIM * ngram_length
    for index in range(MAX_PASSWORD_LENGTH):
        password += gen_character(markov_chain, password[index : index + ngram_length])
        if password[-1] == RIGHT_DELIM:
            return password[:-1].replace(LEFT_DELIM, "")


def cracking_with_markov_chains(
    hashes: list[str], markov_chain: MarkovChain, max_ngrams: int = 3
) -> list[str]:
    """
    Attempt to crack password hashes using a Markov chain-based password generator.

    Iteratively generates passwords using a Markov chain model
    and hashes each generated password. It compares the hashed result against
    a list of provided hash values and returns the cracked plaintext passwords.

    Args:
        hashes (list[str]): A list of hashed values to be cracked.
        markov_chain (MarkovChain): A MarkovChain object used to generate candidate passwords.

    Returns:
        list[str]: A list of cracked plaintext passwords, corresponding to the input hashes.
    """
    plaintext_pass = [None] * len(hashes)
    generated_passwords = set()
    while len(generated_passwords) <= MAX_UNIQUE_PASSWORDS:
        password = generate_password(markov_chain, max_ngrams)
        if password in generated_passwords:
            continue
        generated_passwords.add(password)
        hashed_val = hashlib.sha512(password.encode()).hexdigest()
        print(
            f"Number of Unique passwords generated: {len(generated_passwords):06d}",
            end="\r",
        )
        if hashed_val in hashes:
            index_of_hashed_val = hashes.index(hashed_val)
            plaintext_pass[index_of_hashed_val] = password
    return plaintext_pass


if __name__ == "__main__":
    max_ngrams = 3

    with open("hashes.json") as json_file:
        data = json.load(json_file)

    with open(f"password-data/upto-{max_ngrams}-gram.pickle", "rb") as file:
        markov_chain = pickle.load(file)

    start_time = time.time()
    task4_values = cracking_with_markov_chains(data["task4_hashed_vals"], markov_chain)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task4_values)
