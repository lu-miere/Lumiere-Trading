import os
from passlib.hash import pbkdf2_sha256

_DEFAULT_SCHEME = 'pbkdf2_sha256'
_DEFAULT_ROUNDS = 10000 
_CONTEXT = pbkdf2_sha256.using(rounds=_DEFAULT_ROUNDS)


def hash_password(password:str) -> str :

    return _CONTEXT.hash(password)

def verify_password(password: str, hashedPassword : str) -> bool:
    return _CONTEXT.verify(password, hashedPassword)

