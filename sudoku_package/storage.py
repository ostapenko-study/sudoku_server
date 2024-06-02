"""Storage"""
from sudoku_package.cell import Cell


class Storage:
    """Storage"""

    def __init__(self, values: list[int]):
        self.__cells = []
        for value in values:
            self.__cells.append(Cell(value))

        self.__rows = -1
        self.__cols = -1

    def clear(self) -> None:
        """clear"""
        for cell in self.__cells:
            cell.set_hidden(False)

    def set_shape(self, row: int, col: int) -> None:
        """set shape"""
        self.__rows = row
        self.__cols = col

    def row_count(self) -> int:
        """row count"""
        return self.__rows

    def col_count(self) -> int:
        """cel count"""
        return self.__cols

    def cells(self) -> list[Cell]:
        """get cells"""
        return self.__cells

    def at(self, x: int, y: int) -> Cell:
        """at"""
        return self.__cells[self.index_from_xy(x, y)]

    def index_to_xy(self, index: int) -> tuple[int, int]:
        """index to xy"""
        return (
            index % self.__rows,
            index // self.__rows,
        )

    def xy_by_cell(self, cell: Cell) -> tuple[int, int]:
        """xy by cell"""
        return self.index_to_xy(self.index_by_cell(cell))

    def index_by_cell(self, cell: Cell) -> int:
        """index by cell"""
        return self.__cells.index(cell)

    def index_from_xy(self, x: int, y: int) -> int:
        """index_from_xy"""
        return y * self.__cols + x

    def __str__(self):
        str_var = ""
        for y in range(self.__rows):
            for x in range(self.__cols):
                str_var += self.at(x, y).__str__() + '\t'
            str_var += '\n'
        return str_var
