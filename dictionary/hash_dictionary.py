import hashlib


def hash_file(file_path: str, salt: str = "") -> dict[str, str]:
    """
    Hash all passwords in a file with an optional salt, returning a dictionary of hashed passwords.

    Args:
        file_path (str): The path to the file containing passwords (one per line).
        salt (str, optional): An optional salt to append to each password before hashing. Defaults to "".

    Returns:
        dict[str, str]: A dictionary where the keys are the hashed passwords and the values are the plain text passwords.
    """
    hashed_file = {}
    with open(file_path) as file:
        for password in file:
            clean_pass = password.strip()
            # Do not hash password if already hashed
            if clean_pass in hashed_file.values():
                continue
            hashed_val = hashlib.sha512(f"{clean_pass}{salt}".encode()).hexdigest()
            hashed_file[hashed_val] = clean_pass

    return hashed_file
