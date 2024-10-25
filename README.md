# CS4048 CA - Cracking using N-gram Markov Chains

This project implements a password-cracking algorithm based on Markov Chains. The goal is to generate password guesses that closely resemble real-world password patterns by analyzing a training set of known passwords. Using Markov Chains, the model learns the statistical likelihood of character sequences in passwords, enabling it to generate highly probable password candidates that can be used for password cracking.

## Installation

The project has been tested on python version 3.12.7. Hence, it is suggest to use that version.

External packages **are** required to plot. 

To plot, use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependecies.

```bash
pip install -r requirements.txt
```

## Usage

By default, all of the tasks and imports related to plotting are commented out. You can comment out the distinct tasks within main.py to run specific tasks.

```bash
python main.py

```
