from markov.generate_password import cracking_with_markov_chains
from markov.train_chain import split_into_folds, chain_folds, pickle_markov_chain
from brute_force.crack_brute import brute_force_cracking
from dictionary.crack_dictionary import (
    dictionary_cracking,
    dictionary_cracking_with_salt,
)

# import matplotlib.pyplot as plot
# import seaborn
# import numpy
import json
import time
import pickle
import hashlib


def task_1():
    start_time = time.perf_counter()
    task1_values = brute_force_cracking(data["task1_hashed_vals"])
    elapsed_time = time.perf_counter() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task1_values)


def task_2():
    start_time = time.perf_counter()
    task2_values = dictionary_cracking(
        data["task2_hashed_vals"], "password-data/PasswordDictionary.txt"
    )
    elapsed_time = time.perf_counter() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(task2_values)


def task_3():
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


def task_4_train(folds, max_ngrams):
    for index in range(len(folds)):
        markov_chain = chain_folds(folds[:index] + folds[index + 1 :], max_ngrams)
        # pickling idea came from here https://github.com/brannondorsey/markov-passwords/tree/master
        pickle_markov_chain(
            f"password-data/{dictionary}-{index + 1}-fold-upto-{max_ngrams}-gram.pickle",
            markov_chain,
        )
    return folds


def task_4_crack(folds, max_ngrams):
    success_rates = []
    elapsed_times = []
    for index, fold in enumerate(folds):
        with open(
            f"password-data/{dictionary}-{index + 1}-fold-upto-{max_ngrams}-gram.pickle",
            "rb",
        ) as file:
            markov_chain = pickle.load(file)
        hashed_vals = [
            hashlib.sha512(password.encode()).hexdigest() for password in fold
        ]
        start_time = time.perf_counter()
        cracked_passwords = cracking_with_markov_chains(
            hashed_vals, markov_chain, max_ngrams
        )
        elapsed_time = time.perf_counter() - start_time
        found_passwords = [
            password for password in cracked_passwords if password is not None
        ]
        success_rate = (len(found_passwords) / len(fold)) * 100
        success_rates.append(success_rate)
        elapsed_times.append(elapsed_time)
        print(f"Elapsed time: {elapsed_time} seconds")
        print(f"Fold {index + 1} - Elapsed time: {elapsed_time:.2f} seconds")
        print(f"Passwords cracked: {len(found_passwords)}/{len(fold)}")

    print(f"Average time per fold: {sum(elapsed_times) / len(folds):.2f} seconds")
    print(f"Overall success rate: {sum(success_rates) / len(success_rates):.2f}%")
    return success_rates, elapsed_times


def task_4_plot(success_rates, elapsed_times):

    folds = [1, 2, 3, 4, 5]
    mean_elapsed_times = numpy.mean(elapsed_times)
    std_elaspsed_times = numpy.std(elapsed_times)

    plot.figure(figsize=(8, 6))
    seaborn.barplot(x=folds, y=elapsed_times)

    # Get the positions of the bars as the x-values
    # This is required for centering
    x_pos = numpy.arange(len(folds))

    plot.errorbar(
        x=x_pos,
        y=elapsed_times,
        yerr=[std_elaspsed_times] * len(elapsed_times),
        fmt="o",
        color="black",
        capsize=5,
    )

    # Plot the mean line
    plot.axhline(
        mean_elapsed_times,
        color="red",
        linestyle="--",
        label=f"Mean: {mean_elapsed_times:.2f}%",
    )

    plot.text(
        x=len(elapsed_times) - 0.5,
        y=mean_elapsed_times + 1,
        s=f"Mean: {mean_elapsed_times:.2f}%",
        color="red",
        ha="center",
    )

    plot.title("Elapsed Time per Fold with Mean and Standard Deviation")
    plot.xlabel("Fold Number")
    plot.ylabel("Elapsed Time (seconds)")

    plot.legend()

    plot.savefig("report/images/elapsed-times-with-mean-and-std.png")
    plot.close()

    mean_success_rate = numpy.mean(success_rates)
    std_success_rate = numpy.std(success_rates)

    plot.figure(figsize=(8, 6))
    seaborn.barplot(x=folds, y=success_rates)

    plot.errorbar(
        x=x_pos,
        y=success_rates,
        yerr=[std_success_rate] * len(success_rates),
        fmt="o",
        color="black",
        capsize=5,
    )

    # Plot the mean line
    plot.axhline(
        mean_success_rate,
        color="red",
        linestyle="--",
        label=f"Mean: {mean_success_rate:.2f}%",
    )

    plot.text(
        x=len(success_rates) - 0.5,
        y=mean_success_rate + 1,
        s=f"Mean: {mean_success_rate:.2f}%",
        color="red",
        ha="center",
    )

    plot.title("Success Rate per Fold with Mean and Standard Deviation")
    plot.xlabel("Fold Number")
    plot.ylabel("Success Rate (%)")

    plot.legend()

    plot.savefig("report/images/success-rate-with-mean-and-std.png")
    plot.close()


if __name__ == "__main__":

    with open("hashes.json") as json_file:
        data = json.load(json_file)

    # task_1()
    # task_2()
    # task_3()

    num_folds = 5
    max_ngrams = 3
    dictionary = "rockyou.txt"
    folds = split_into_folds(f"password-data/{dictionary}", num_folds)
    task_4_train(folds, max_ngrams)
    success_rates, elapsed_times = task_4_crack(folds, max_ngrams)
    # task_4_plot(success_rates, elapsed_times)
