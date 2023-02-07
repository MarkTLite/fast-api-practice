from passlib.context import CryptContext

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


class Hash:
    """Blueprint for hashing objects"""

    def bcrypt(password: str):
        """create and return bcrypt based hash"""
        return pwd_context.hash(secret=password)

    def verify(hashed_pass, plain_pass):
        return pwd_context.verify(secret=plain_pass, hash=hashed_pass)
