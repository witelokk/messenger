from hashlib import sha256


def hash_password(password: str):
    return sha256(password.encode()).hexdigest()
