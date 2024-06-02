"""test module"""
import random

from api import solve, Data, run
from authorization import UserDatabase, User, is_user, generate_token, get_user_by_token
from sudoku_package.checker_generators import generate_main_checkers
from sudoku_package.task_generator import task_generator

N = 5


def test_true_integration():
    """true_integration"""
    for i in range(N):
        print(f'test_integration {i + 1}')
        data = Data.model_validate(task_generator(random.randint(1, 9999999)))
        result = solve(data, generate_main_checkers)
        assert result
        result2 = run(data, generate_main_checkers)
        assert result2["result"]


def test_false_integration():
    """false_integration"""
    for item in [
        {
            "cols": 3,
            "rows": 3,
            "numbers": [
                1, 1, 1,
                1, 1, 1,
                1, 1, 1,
            ]
        },
    ]:
        data = Data.model_validate(item)

        result = solve(data, generate_main_checkers)
        assert not result
        result2 = run(data, generate_main_checkers)
        assert not result2["result"]


def generate_array(count):
    """generate_array"""
    return list(range(count))


def test_false_api_model():
    """false_api_model"""
    for item in [
        {
            "row": 3,
            "col": 3,
            "numbers": generate_array(9)
        },
        {
            "rows": 1,
            "cols": 3,
            "numbers": generate_array(3)
        },
        {
            "rows": 3,
            "cols": 1,
            "numbers": generate_array(3)
        },
        {
            "rows": 3,
            "cols": 3,
            "numbers": generate_array(8)
        },
        {
            "rows": 3,
            "cols": 3,
            "numbers": generate_array(10)
        },
        {
            "rows": 3,
            "cols": 30,
            "numbers": generate_array(89)
        },
        {
            "rows": 700,
            "cols": 30,
            "numbers": generate_array(700 * 30 + 1)
        },
        {
            "rows": -1,
            "cols": 3,
            "numbers": generate_array(9)
        },
        {
            "rows": 6,
            "cols": -2,
            "numbers": generate_array(9)
        },
        {
            "rows": 3,
            "cols": 3,
            "numbers": None
        },
        {
            "rows": None,
            "cols": 3,
            "numbers": generate_array(9)
        },
	{
            "rows": None,
            "cols": 3,
            "numbers": generate_array(9)
        },
    ]:
        try:
            Data.model_validate(item)
            print(item)
            assert False
        except ValueError:
            assert True


def test_true_api_model():
    """true_api_model"""
    for item in [
        {
            "rows": 3,
            "cols": 3,
            "numbers": generate_array(9)
        },
        {
            "rows": 3,
            "cols": 30,
            "numbers": generate_array(90)
        },
        {
            "rows": 700,
            "cols": 30,
            "numbers": generate_array(700 * 30)
        }
    ]:
        try:
            Data.model_validate(item)
            assert True
        except ValueError:
            assert False


def test_authorization_user():
    """!!!"""
    test_db_filename = "test_data.db"
    user_db = UserDatabase(test_db_filename)
    User.drop()
    User.create()
    user = {"username": "test_user", "password": "test_pass"}
    assert not user_db.is_user(user)
    assert not is_user(user, test_db_filename)
    user_db.add(user)
    assert user_db.is_user(user)
    assert is_user(user, test_db_filename)
    user_db.clear()
    assert not user_db.is_user(user)
    assert not is_user(user, test_db_filename)


def test_authorization_token():
    """!!!"""
    for user in [
        {"username": "test_user", "password": "test_pass"},
        {"username": "admin", "password": "admin"},
        {"username": "123", "password": "987"},
        {"username": "!@#$", "password": "qwe"},
        {"username": "asd", "password": "((*&^))"},
    ]:
        token = generate_token(user)
        assert user == get_user_by_token(token)
