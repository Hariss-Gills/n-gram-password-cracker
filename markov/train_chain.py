import pickle
import random
from collections import defaultdict
from typing import DefaultDict, List, TypeAlias

MarkovChain: TypeAlias = DefaultDict[str, DefaultDict[str, float]]

# Use non-ascii chars as delimeters
LEFT_DELIM = "£"
RIGHT_DELIM = "€"


def find_ngram(password: str, ngram_length: int) -> list[tuple[str, str]]:
    """
     Generate n-grams from a password string.

     An n-gram consists of a prefix of `ngram_length` characters and the
     character that follows it. For prefixes shorter than `ngram_length`,
     the prefix is left-padded with the £ character.

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


def split_into_folds(file_path: str, num_folds: int = 5):
    """
    Splits the data from a file into randomized folds, ensuring randomness in the data distribution,

    Args:
        file_path (str): Path to the file containing the data, with one entry per line.
        num_folds (int, optional): Number of folds to split the data into. Defaults to 5.

    Returns:
        list[list[str]]: A list containing folds, where each fold is a list of strings (lines from the file).

    """
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    random.shuffle(lines)

    folds = []
    fold_size = len(lines) // num_folds
    remainder = len(lines) % num_folds

    start = 0
    for i in range(num_folds):
        end = start + fold_size + (1 if i < remainder else 0)
        folds.append(lines[start:end])
        start = end

    return folds


def chain_folds(folds: list[list[str]], max_ngrams: int = 3) -> MarkovChain:
    """
    Builds a Markov chain model from a list of folds, where each fold contains password sequences.

    Each line of the fold is treated as a string, and n-grams are generated
    for it. The function builds a Markov chain that captures the transition
    probabilities between characters.

    Args:
        folds (list[list[str]]): A list of folds, where each fold is a list of strings representing passwords.
        max_ngrams (int, optional): The maximum length of n-grams to consider for the Markov chain. Defaults to 3.

    Returns:
        MarkovChain: The Markov chain built from the file contents.
    """
    markov_chain: MarkovChain = defaultdict(defaultdict(float).copy)
    for fold in folds:
        for password in fold:
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
    folds = split_into_folds("password-data/rockyou.txt", 5)
    for index, fold in enumerate(folds):
        markov_chain = chain_folds(folds[:index] + folds[index + 1 :])
        print(markov_chain)
        # pickling idea came from here https://github.com/brannondorsey/markov-passwords/tree/master
        pickle_markov_chain(
            f"password-data/{index + 1}-upto-{max_ngrams}-gram.pickle", markov_chain
        )
