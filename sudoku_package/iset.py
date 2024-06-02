"""ISet"""
from abc import ABC, abstractmethod

from sudoku_package.cell import Cell
from sudoku_package.set_cells import SetCells


class ISet(ABC):
    """ISet"""

    def __init__(self):
        pass

    @abstractmethod
    def is_correct(self) -> bool:
        """is_correct"""

    @abstractmethod
    def has_cell(self, cell: Cell) -> bool:
        """has_cell"""

    @abstractmethod
    def get_not_compatibility_sets_cells(self, cell: Cell) -> list[SetCells]:
        """get_not_compatibility_sets_cells"""
