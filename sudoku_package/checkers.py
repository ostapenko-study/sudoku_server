"""checkers"""
from abc import ABC
import itertools
from sudoku_package.block import Block
from sudoku_package.cell import Cell
from sudoku_package.iset import ISet
from sudoku_package.set_cells import SetCells
from sudoku_package.storage import Storage


def prepare_not_compatibility_cells(data: list[SetCells]):
    """prepare data"""
    return data


class Checker(ISet, ABC):
    """Checker"""

    def __init__(self, sets: list[ISet]):
        super().__init__()
        self.__sets = sets

    def has_cell(self, cell: Cell) -> bool:
        """has cell"""
        for item in self.__sets:
            if item.has_cell(cell):
                return True
        return False


class ConjunctionChecker(Checker):
    """ConjunctionChecker"""

    def __init__(self, sets: list[ISet]):
        super().__init__(sets)
        self.__sets = sets

    def is_correct(self) -> bool:
        """is_correct"""
        for item in self.__sets:
            if not item.is_correct():
                print(item)
                return False

        return True

    def get_not_compatibility_sets_cells(self, cell: Cell) -> list[SetCells]:
        """get_not_compatibility_sets_cells"""
        sets = []
        new_sets = []
        for item in self.__sets:
            if item.has_cell(cell):
                tmp = item.get_not_compatibility_sets_cells(cell)
                if len(tmp) == 0:
                    continue
                new_sets += tmp
                for set_cells in tmp:
                    if len(set_cells):
                        sets.append(set_cells)
        if len(sets) == 0:
            return []
        if len(new_sets) > 1:
            new_answer = [SetCells(set(var)) for var in itertools.product(*new_sets)]
            return prepare_not_compatibility_cells(new_answer)

        return prepare_not_compatibility_cells([SetCells(set(new_sets[0]))])


class DisjunctionChecker(Checker):
    """DisjunctionChecker"""

    def __init__(self, sets: list[ISet]):
        super().__init__(sets)
        self.__sets = sets

    def is_correct(self) -> bool:
        for item in self.__sets:
            if item.is_correct():
                return True

        return False

    def get_not_compatibility_sets_cells(self, cell: Cell) -> list[SetCells]:
        answer = []
        for item in self.__sets:
            if item.has_cell(cell):
                for set_cells in item.get_not_compatibility_sets_cells(cell):
                    if len(set_cells):
                        answer.append(set_cells)
                    else:
                        return []
            else:
                return []
        return prepare_not_compatibility_cells(answer)


def generate_row_checker(storage: Storage) -> ISet:
    """generate_row_checker"""
    blocks = []
    for y in range(storage.row_count()):
        cells = []
        for x in range(storage.col_count()):
            cells.append(storage.at(x, y))
        blocks.append(Block(cells))
    return ConjunctionChecker(blocks)


def generate_col_checker(storage: Storage) -> ISet:
    """generate_col_checker"""
    blocks = []
    for x in range(storage.col_count()):
        cells = []
        for y in range(storage.row_count()):
            cells.append(storage.at(x, y))
        blocks.append(Block(cells))
    return ConjunctionChecker(blocks)


def generate_mini_checker(storage: Storage, block_size: int = 3) -> ISet:
    """generate_mini_checker"""
    if storage.row_count() % block_size:
        raise AttributeError("storage.rowCount() % block_size")
    if storage.col_count() % block_size:
        raise AttributeError("storage.colCount() % block_size")

    blocks = []

    max_x = storage.row_count() // block_size
    max_y = storage.col_count() // block_size

    for x in range(max_x):
        for y in range(max_y):
            cells = []
            for dx in range(block_size):
                for dy in range(block_size):
                    cells.append(storage.at(x * block_size + dx, y * block_size + dy))

            blocks.append(Block(cells))

    return ConjunctionChecker(blocks)
