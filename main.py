from markov.generate_password import cracking_with_markov_chains
from brute_force.generate_password import brute_force_cracking
from dictionary.crack_dictionary import (
    dictionary_cracking,
    dictionary_cracking_with_salt,
)
import json
import time
import pickle


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
