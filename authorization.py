"""
authorization
"""
import hashlib
import jwt
import orm_sqlite
from passlib.context import CryptContext
from config import DATABASE_FILE


class User(orm_sqlite.Model):
    """!!!"""
    id = orm_sqlite.IntegerField(primary_key=True)
    username = orm_sqlite.StringField()
    password_hash = orm_sqlite.StringField()

    objects = None  # E1101


def dict_to_user(user):
    """!!!"""
    return {
        'username': user["username"],
        'password_hash': hashlib.md5(user['password'].encode('utf-8')).hexdigest()
    }


class UserDatabase:
    """!!!"""

    def __init__(self, db_file):
        """!!!"""
        self.__db = orm_sqlite.Database(db_file)
        User.objects.backend = self.__db

    def clear(self):
        """!!!"""
        User.drop()

    def add(self, user: dict):
        """!!!"""
        User.objects.add(dict_to_user(user))

    def is_user(self, user):
        """!!!"""
        user = dict_to_user(user)
        if not User.exists():
            return False
        return len(User.objects.find(
            filter=f'username="{user["username"]}" AND password_hash="{user["password_hash"]}"'
        )) != 0


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def is_user(user, db_filename=DATABASE_FILE):
    """!!!"""
    __db = UserDatabase(db_filename)
    return __db.is_user(user)


def generate_token(user):
    """!!!"""
    return jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_token(jwt_token):
    """!!!"""
    return jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])

#
# if __name__ == "__main__":
#     db = UserDatabase(DATABASE_FILE)
#     User.drop()
#     User.create()
#     db.add({"username": "admin", "password": "123"})
