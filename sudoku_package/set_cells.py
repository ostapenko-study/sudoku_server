"""SetCells"""
from sudoku_package.cell import Cell


class SetCells(set[Cell]):
    """SetCells"""

    def __init__(self, cells: set[Cell]):
        super().__init__(cells)
        self.__cache = []
        for cell in self:
            if not cell.is_hidden():
                self.__cache.append(cell)

    def is_all_hidden(self):
        """is_all_hidden"""
        for cell in self:
            if not cell.is_hidden():
                return False
        return True

    def install_all_hidden(self):
        """stall_all_hidden"""
        for cell in self.__cache:
            cell.set_hidden(True)

        if not self.is_all_hidden():
            raise AttributeError

    def restore(self):
        """restore"""
        for cell in self.__cache:
            cell.set_hidden(False)
