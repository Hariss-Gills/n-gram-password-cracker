from string import ascii_lowercase, digits
from itertools import product
import hashlib

CHARS = ascii_lowercase + digits

def generate_lex_order_at_len(alphabet: str, length: int) -> list[str]:
    lex_order_at_len = []
    
    for combination in product(alphabet, repeat=length):
            lex_order_at_len.append(''.join(combination))

    return lex_order_at_len


def brute_force_cracking(hashes: list[str]) -> list[str]:
    plaintext_pass = [None] * len(hashes)
    shortlex_order = []
    length = 0
    
    while True:
        if None not in plaintext_pass:
            break
        
        shortlex_order += generate_lex_order_at_len(CHARS, length)
        for string in shortlex_order:
            hashed_val = hashlib.sha512(string.encode()).hexdigest()
            if hashed_val in hashes:
                index_of_hashed_val = hashes.index(hashed_val)
                plaintext_pass[index_of_hashed_val] = string
        length += 1

    return plaintext_pass



if __name__ == '__main__':
    hashed_vals = [
'f14aae6a0e050b74e4b7b9a5b2ef1a60ceccbbca39b132ae3e8bf88d3a946c6d8687f3266fd2b626419d8b67dcf1d8d7c0fe72d4919d9bd05efbd37070cfb41a',
'e85e639da67767984cebd6347092df661ed79e1ad21e402f8e7de01fdedb5b0f165cbb30a20948f1ba3f94fe33de5d5377e7f6c7bb47d017e6dab6a217d6cc24',
'4e2589ee5a155a86ac912a5d34755f0e3a7d1f595914373da638c20fecd7256ea1647069a2bb48ac421111a875d7f4294c7236292590302497f84f19e7227d80',
'afd66cdf7114eae7bd91da3ae49b73b866299ae545a44677d72e09692cdee3b79a022d8dcec99948359e5f8b01b161cd6cfc7bd966c5becf1dff6abd21634f4b'
    ]
    values = brute_force_cracking(hashed_vals)
    for val in values:
        print(val)


     
