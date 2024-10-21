from markov.generate_password import cracking_with_markov_chains
from markov.train_chain import split_into_folds, chain_folds, pickle_markov_chain
from brute_force.crack_brute import brute_force_cracking
from dictionary.crack_dictionary import (
    dictionary_cracking,
    dictionary_cracking_with_salt,
)
import json
import time
import pickle
import hashlib
import argparse


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="CS4028 - Assesment")
    # parser.add_argument("task", help="Task you would like to run",
    #    type=int,
    #    choices=[1,2,3,4],
    #    nargs='+')
    # args = parser.parse_args()
    # print(args.task)
    with open("hashes.json") as json_file:
        data = json.load(json_file)

    start_time = time.perf_counter()
    task1_values = brute_force_cracking(data["task1_hashed_vals"])
    elapsed_time = time.perf_counter() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task1_values)

    start_time = time.perf_counter()
    task2_values = dictionary_cracking(
        data["task2_hashed_vals"], "password-data/PasswordDictionary.txt"
    )
    elapsed_time = time.perf_counter() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task2_values)

    # Python annotingly has no built in way to store tuples from json
    # https://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json
    task3_hashed_vals = data["task3_hashed_vals"]
    for index, item in enumerate(task3_hashed_vals):
        task3_hashed_vals[index] = tuple(item)

    start_time = time.perf_counter()
    task3_values = dictionary_cracking_with_salt(
        data["task3_hashed_vals"], "password-data/PasswordDictionary.txt"
    )
    elapsed_time = time.perf_counter() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task3_values)

    # Train for task 4
    max_ngrams = 3
    num_folds = 5
    dictionary = "rockyou.txt"
    folds = split_into_folds(f"password-data/{dictionary}", num_folds)
    for index, fold in enumerate(folds):
        markov_chain = chain_folds(folds[:index] + folds[index + 1 :], max_ngrams)
        # pickling idea came from here https://github.com/brannondorsey/markov-passwords/tree/master
        pickle_markov_chain(
            f"password-data/{dictionary}-{index + 1}-fold-upto-{max_ngrams}-gram.pickle",
            markov_chain,
        )

    # Attempt to crack
    total_passwords = 0
    total_found = 0
    total_time = 0
    for index, fold in enumerate(folds):
        with open(
            f"password-data/{dictionary}-{index + 1}-fold-upto-{max_ngrams}-gram.pickle",
            "rb",
        ) as file:
            markov_chain = pickle.load(file)
        hashed_vals = []
        for password in fold:
            hashed_val = hashlib.sha512(password.encode()).hexdigest()
            hashed_vals.append(hashed_val)
        start_time = time.perf_counter()
        cracked_passwords = cracking_with_markov_chains(hashed_vals, markov_chain)
        elapsed_time = time.perf_counter() - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        print(f"Fold {index + 1} - Elapsed time: {elapsed_time:.2f} seconds")
        print(
            f"Passwords cracked: {len(
            [password for password in cracked_passwords if password is not None]
        )}/{len(fold)}"
        )
        total_time += elapsed_time
        total_found += len(
            [password for password in cracked_passwords if password is not None]
        )
        total_passwords += len(fold)

    # Calculate final metrics
    average_time = total_time / 5
    success_rate = (total_found / total_passwords) * 100

    print(f"Average time per fold: {average_time:.2f} seconds")
    print(f"Overall success rate: {success_rate:.2f}%")
