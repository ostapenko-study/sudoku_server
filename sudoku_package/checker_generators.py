"""!!!"""
from sudoku_package.checkers import ConjunctionChecker, \
    generate_row_checker, generate_col_checker, generate_mini_checker
from sudoku_package.iset import ISet
from sudoku_package.storage import Storage


def generate_sudoku_checker(storage: Storage, block_size: int = 3) -> ISet:
    """generate_sudoku_checker"""
    return ConjunctionChecker([
        generate_mini_checker(storage, block_size=block_size),
        generate_col_checker(storage),
        generate_row_checker(storage)
    ])


def generate_base_checkers(storage: Storage) -> list[tuple[str, ISet]]:
    """generate_base_checkers"""
    return [
        # ("row or col", DisjunctionChecker([
        #     generate_col_checker(storage),
        #     generate_row_checker(storage)
        # ])),
        ("row and col", ConjunctionChecker([
            generate_col_checker(storage),
            generate_row_checker(storage)
        ])),
        ("row", generate_row_checker(storage)),
        ("col", generate_col_checker(storage))
    ]


def generate_main_checker(storage: Storage, block_size: int = 3) -> list[tuple[str, ISet]]:
    """generate_main_checker"""
    return [
        (
            "main_checker", ConjunctionChecker(
                [
                    generate_mini_checker(storage, block_size=block_size),
                    ConjunctionChecker([
                        generate_col_checker(storage),
                        generate_row_checker(storage)
                    ])
                ]
            ),
        )
    ]


def generate_main_checkers(storage: Storage, block_size: int = 3) -> list[tuple[str, ISet]]:
    """generate_main_checkers"""
    return [
        (data[0],
         ConjunctionChecker([
             generate_mini_checker(storage, block_size=block_size), data[1]
         ])
         )
        for data in generate_base_checkers(storage)
    ]
