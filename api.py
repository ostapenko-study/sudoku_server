"""!!!"""
import random
from typing import List, Annotated

import fastapi
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, field_validator, ValidationInfo, model_validator
from typing_extensions import Self

from authorization import is_user, generate_token, get_user_by_token
from sudoku_package.checker_generators import generate_main_checkers
from sudoku_package.solver import Solver
from sudoku_package.storage import Storage
from sudoku_package.task_generator import task_generator


class Data(BaseModel):
    """Data"""
    cols: int
    rows: int
    numbers: List[int]

    @field_validator('cols', 'rows')
    @classmethod
    def check_row_and_col(cls, v: int, info: ValidationInfo) -> str:
        """check row and col"""
        if isinstance(v, int):
            if v < 2:
                raise ValueError(f"invalid {info.field_name}")

        return v

    @model_validator(mode="after")
    def check_matrix_size(self) -> Self:
        """check matrix size"""
        if len(self.numbers) != self.cols * self.rows:
            raise ValueError("invalid matrix")
        return self


app = fastapi.FastAPI()


def solve(data: Data, generator):
    """!!!"""
    st = Storage(data.numbers)
    st.set_shape(data.rows, data.cols)
    checkers = generator(st)
    for checker in checkers:
        solver = Solver(st, checker[1])
        result = solver.solve()
        if result:
            return result
    return None


def run(data: Data, function_generator):
    """!!!"""
    result = solve(data, function_generator)
    if result:
        return {"result": result}
    return {"result": False}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """!!!"""
    user = {
        "username": form_data.username,
        "password": form_data.password,
    }
    if is_user(user):
        return {
            "access_token": generate_token(user),
            "token_type": "bearer"
        }
    raise HTTPException(403)


@app.get("/main_rules")
def get_main_rules():
    """generate task"""
    return task_generator(random.randint(1, 99999999999))


@app.get("/main_rules/{item_id}")
def get_main_rules_by_id(item_id):
    """generate task"""
    return task_generator(int(item_id))


@app.post("/main_rules")
def pos_main_rules(data: Data, token: Annotated[str, fastapi.Depends(oauth2_scheme)]):
    """solve task"""
    if not is_user(get_user_by_token(token)):
        raise HTTPException(401)
    return run(data, generate_main_checkers)
