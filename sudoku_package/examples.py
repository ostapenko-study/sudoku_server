"""examples"""
from sudoku_package.checker_generators import generate_main_checkers
from sudoku_package.iset import ISet
from sudoku_package.storage import Storage
from sudoku_package.solver import Solver


def run_example(storage: Storage, checkers: list[tuple[str, ISet]]):
    """example runner"""
    print("input:")
    print(storage)

    for idx, checker in enumerate(checkers):
        print(idx + 1, ":", checker[0])
        storage.clear()
        solver = Solver(storage, checker[1])
        result = solver.solve()
        if result:
            print("Solution was found")
            print(storage)
            print(result)
            print("Is correct by checker:", checker[1].is_correct())
            print("Is correct by combination:", solver.check_combination())
        else:
            print("There are no solutions")


def main_example():
    """main example"""
    storage = Storage(
        [
            3, 9, 6, 2, 5, 1, 6, 8, 7,
            6, 1, 2, 7, 3, 3, 4, 9, 5,
            7, 3, 9, 8, 6, 9, 7, 2, 5,
            3, 7, 5, 1, 8, 4, 2, 7, 8,
            9, 8, 8, 6, 7, 4, 5, 1, 4,
            1, 5, 9, 3, 5, 8, 1, 6, 4,
            5, 4, 1, 2, 2, 6, 8, 7, 9,
            2, 2, 3, 5, 4, 3, 6, 5, 1,
            4, 6, 8, 7, 1, 9, 7, 3, 2,
        ]
    )

    storage.set_shape(9, 9)
    checkers = generate_main_checkers(storage, block_size=3)

    run_example(storage, checkers)
