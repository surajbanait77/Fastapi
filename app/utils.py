from passlib.context import CryptContext
'''hashed the password'''
pwd_context = CryptContext(schemes={"bcrypt"}, deprecated='auto')  # Tells passlib which alg we want to use "bcrypt"        


def hash(password: str):   # hashes the password
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) # compares the password for user login