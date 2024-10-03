from string import ascii_lowercase, digits
from itertools import product
import hashlib

CHARS = ascii_lowercase + digits

def generate_lex_order_at_len(alphabet: str, length: int) -> list[str]:
    lex_order_at_len = []
    
    for combination in product(alphabet, repeat=length):
            lex_order_at_len.append(''.join(combination))

    return lex_order_at_len


# TODO: make more efficent with loading it with parallelism
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

# TODO: make more efficent with loading it in chunks and parallelism
def hash_file(file_path: str) -> dict[str, str]:
    # Load in line by line
    hashed_file = {}
    try:
        with open(file_path) as file:
            for password in file:
                clean_pass = password.strip()
                hashed_val = hashlib.sha512(clean_pass.encode()).hexdigest() 
                hashed_file[hashed_val] = clean_pass
    except FileNotFoundError:
        # Download file from GitHub
        print("Error: The file was not found.")
    except PermissionError:
        # Change permission
        print("Error: You do not have permission to read the file.")
    return hashed_file

def dictionary_cracking(hashes: list[str]) -> list[str]:
    plaintext_pass = [None] * len(hashes)
    hashed_file = hash_file("PasswordDictionary.txt")
    for index in range(len(hashes)):
        #if hashes[index] in plaintext_pass:
        #    continue
        if hashes[index] in hashed_file:
            plaintext_pass[index] = hashed_file[hashes[index]]

    return plaintext_pass

if __name__ == '__main__':
    hashed_vals = [
'f14aae6a0e050b74e4b7b9a5b2ef1a60ceccbbca39b132ae3e8bf88d3a946c6d8687f3266fd2b626419d8b67dcf1d8d7c0fe72d4919d9bd05efbd37070cfb41a',
'e85e639da67767984cebd6347092df661ed79e1ad21e402f8e7de01fdedb5b0f165cbb30a20948f1ba3f94fe33de5d5377e7f6c7bb47d017e6dab6a217d6cc24',
'4e2589ee5a155a86ac912a5d34755f0e3a7d1f595914373da638c20fecd7256ea1647069a2bb48ac421111a875d7f4294c7236292590302497f84f19e7227d80',
'afd66cdf7114eae7bd91da3ae49b73b866299ae545a44677d72e09692cdee3b79a022d8dcec99948359e5f8b01b161cd6cfc7bd966c5becf1dff6abd21634f4b'
    ]
    values = brute_force_cracking(hashed_vals)
    print(values)
    test = ['31a3423d8f8d93b92baffd753608697ebb695e4fca4610ad7e08d3d0eb7f69d75cb16d61caf7cead0546b9be4e4346c56758e94fc5efe8b437c44ad460628c70',
'9381163828feb9072d232e02a1ee684a141fa9cddcf81c619e16f1dbbf6818c2edcc7ce2dc053eec3918f05d0946dd5386cbd50f790876449ae589c5b5f82762',
'a02f6423e725206b0ece283a6d59c85e71c4c5a9788351a24b1ebb18dcd8021ab854409130a3ac941fa35d1334672e36ed312a43462f4c91ca2822dd5762bd2b',
'834bd9315cb4711f052a5cc25641e947fc2b3ee94c89d90ed37da2d92b0ae0a33f8f7479c2a57a32feabdde1853e10c2573b673552d25b26943aefc3a0d05699',
'0ae72941b22a8733ca300161619ba9f8314ccf85f4bad1df0dc488fdd15d220b2dba3154dc8c78c577979abd514bf7949ddfece61d37614fbae7819710cae7ab',
'6768082bcb1ad00f831b4f0653c7e70d9cbc0f60df9f7d16a5f2da0886b3ce92b4cc458fbf03fea094e663cb397a76622de41305debbbb203dbcedff23a10d8a',
'0f17b11e84964b8df96c36e8aaa68bfa5655d3adf3bf7b4dc162a6aa0f7514f32903b3ceb53d223e74946052c233c466fc0f2cc18c8bf08aa5d0139f58157350',
'cf4f5338c0f2ccd3b7728d205bc52f0e2f607388ba361839bd6894c6fb8e267beb5b5bfe13b6e8cc5ab04c58b5619968615265141cc6a8a9cd5fd8cc48d837ec',
'1830a3dfe79e29d30441f8d736e2be7dbc3aa912f11abbffb91810efeef1f60426c31b6d666eadd83bbba2cc650d8f9a6393310b84e2ef02efa9fe161bf8f41d',
'3b46175f10fdb54c7941eca89cc813ddd8feb611ed3b331093a3948e3ab0c3b141ff6a7920f9a068ab0bf02d7ddaf2a52ef62d8fb3a6719cf25ec6f0061da791']
    yo = dictionary_cracking(test)
    print(yo)

     
