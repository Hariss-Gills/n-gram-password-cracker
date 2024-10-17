import pickle
from collections import defaultdict
from typing import DefaultDict, TypeAlias

MarkovChain: TypeAlias = DefaultDict[str, DefaultDict[str, float]]

# Use non-ascii chars as delimeters
LEFT_DELIM = "£"
RIGHT_DELIM = "€"


def find_ngram(password: str, ngram_length: int) -> list[tuple[str, str]]:
    """
    Generate n-grams from a password string.

    An n-gram consists of a prefix of `ngram_length` characters and the
    character that follows it. For prefixes shorter than `ngram_length`,
    the prefix is left-padded with the `^` character.

    Args:
        password (str): The string from which to generate n-grams.
        ngram_length (int): The length of the n-gram to generate.

    Returns:
        list[tuple[str, str]]: A list of (prefix, character) tuples representing the n-grams.
    """
    ngrams = []
    for index in range(len(password)):
        if index < ngram_length:
            # left delimeter with "£"
            prefix = LEFT_DELIM * (ngram_length - index) + password[:index]
            ngrams.append((prefix, password[index]))
        else:
            ngrams.append((password[index - ngram_length : index], password[index]))
    return ngrams


def find_token_occurence(
    password: str, max_ngrams: int, markov_chain: MarkovChain
) -> None:
    """
    Process a string and update the Markov chain with its n-grams.

    For each n-gram length from 1 to `max_ngrams`, the function generates
    n-grams from `password` and updates the Markov chain with their counts.

    Args:
        password (str): The string to process.
        max_ngrams (int): The maximum length of n-grams to generate.
        markov_chain (MarkovChain): The Markov chain to update with n-gram counts.
    """
    for n in range(1, max_ngrams + 1):
        for prev, next in find_ngram(password, n):
            # avoid key errors here by using a defaultdict
            # https://docs.python.org/3/library/collections.html#collections.defaultdict
            markov_chain[prev][next] += 1


def calculate_probabilities(markov_chain: MarkovChain) -> None:
    """
    Convert counts in the Markov chain to probabilities.

    Normalizes the counts of transitions from each prefix so that
    they sum to 1, turning them into probabilities.

    Args:
        markov_chain (MarkovChain): The Markov chain with n-gram probabilities.
    """
    for prev, next_chars in markov_chain.items():
        total_count = sum(next_chars.values())
        for next, count in next_chars.items():
            markov_chain[prev][next] = count / total_count


def chain_file(file_path: str) -> MarkovChain:
    """
    Load a file and build a Markov chain from its contents.

    Each line of the file is treated as a string, and n-grams are generated
    for it. The function builds a Markov chain that captures the transition
    probabilities between characters.

    Args:
        file_path (str): The path to the file containing strings to process.

    Returns:
        MarkovChain: The Markov chain built from the file contents.
    """
    markov_chain: MarkovChain = defaultdict(defaultdict(float).copy)
    with open(file_path, "r") as file:
        # Use € as right delimeter
        for password in file:
            password = password.strip()
            password += RIGHT_DELIM
            find_token_occurence(password, max_ngrams, markov_chain)

    calculate_probabilities(markov_chain)
    return markov_chain


def pickle_markov_chain(file_path: str, markov_chain: MarkovChain) -> None:
    """
    Save a markov chain to a file using pickle.

    The function serializes the Markov chain as a binary file, allowing it
    to be loaded later.

    Args:
        file_path (str): The path to the output pickle file.
        markov_chain (MarkovChain): The Markov chain to serialize and save.
    """
    with open(file_path, "wb") as file:
        pickle.dump(markov_chain, file)


if __name__ == "__main__":
    max_ngrams = 3
    markov_chain = chain_file("password-data/PasswordDictionary.txt")
    print(markov_chain)
    # pickling idea came from here https://github.com/brannondorsey/markov-passwords/tree/master
    pickle_markov_chain(f"password-data/upto-{max_ngrams}-gram.pickle", markov_chain)
