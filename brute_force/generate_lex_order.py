from itertools import product


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
