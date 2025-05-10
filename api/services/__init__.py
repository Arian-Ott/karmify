from passlib.context import CryptContext

crypto_context = CryptContext(schemes=["argon2"], deprecated="auto")
