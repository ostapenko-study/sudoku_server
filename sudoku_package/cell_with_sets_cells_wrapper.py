"""!!!"""
from sudoku_package.cell import Cell
from sudoku_package.sets_cells_wrapper import SetsCellsWrapper, generate_sets_cells_wrapper


class CellWithSetsCellsWrapper:
    """!!!"""

    def __init__(self, cell: Cell, sets: SetsCellsWrapper):
        self.__cell = cell
        self.__sets = sets
        self.__current_index = -1

    def is_needed_to_solve(self) -> bool:
        """!!!"""
        if self.__cell.is_hidden():
            return False
        return self.__sets.is_needed_to_solve()

    def has_next_state(self) -> bool:
        """!!!"""
        if self.__current_index == -1:
            return True
        return self.__sets.is_needed_to_solve()

    def go_to_the_next_state(self) -> None:
        """!!!"""
        if not self.has_next_state():
            raise AttributeError
        if self.__current_index == -1:
            self.__current_index = 0
            self.__cell.set_hidden(True)
        else:
            self.__cell.set_hidden(False)
            self.__sets.go_to_the_next_state()

    def restore_hidden_cells(self) -> None:
        """!!!"""
        self.__cell.set_hidden(False)
        self.__sets.restore_hidden_cells()

    def to_data(self) -> tuple[Cell, list[set[Cell]]]:
        """!!!"""
        return self.__cell, self.__sets.sets_cells()


def generate_cell_with_sets_cells_wrapper(data: tuple[Cell, list[set[Cell]]]):
    """!!!"""
    return CellWithSetsCellsWrapper(data[0], generate_sets_cells_wrapper(data[1]))
