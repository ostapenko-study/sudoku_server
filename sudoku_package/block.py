"""!!!"""
from sudoku_package.iset import ISet
from sudoku_package.cell import Cell


class Block(ISet):
    """!!!"""
    def __init__(self, cells: list[Cell]):
        super().__init__()
        self.__cells = cells

    def is_correct(self) -> bool:
        """!!!"""
        values = set()
        for cell in self.__cells:
            if cell.is_hidden():
                continue
            if cell.value() in values:
                return False
            values.add(cell.value())
        return True

    def has_cell(self, cell: Cell) -> bool:
        """!!!"""
        return cell in self.__cells

    def get_not_compatibility_sets_cells(self, cell: Cell) -> list[set[Cell]]:
        """!!!"""
        if cell not in self.__cells:
            return [set()]

        answer = set()
        for item in self.__cells:
            if cell.value() == item.value() and cell is not item:
                answer.add(item)
        return [answer]

    def __str__(self):
        """!!!"""
        return "BLOCK: " + [cell.value() for cell in self.__cells].__str__()
