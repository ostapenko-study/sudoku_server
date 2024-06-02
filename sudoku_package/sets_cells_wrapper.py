"""SetsCellsWrapper"""
from sudoku_package.cell import Cell
from sudoku_package.set_cells import SetCells


class SetsCellsWrapper:
    """SetsCellsWrapper"""

    def __init__(self, sets_cells: list[SetCells]):
        self.__sets_cells = sets_cells
        self.__sets_cells_cache = []
        for set_cells in sets_cells:
            tmp = set()
            for cell in set_cells:
                if not cell.is_hidden():
                    tmp.add(cell)
            self.__sets_cells_cache.append(tmp)

        self.__current_index = -1

    def sets_cells(self) -> list[SetCells]:
        """sets_cells"""
        return self.__sets_cells

    def has_next_state(self):
        """has_next_state"""
        return self.__current_index < len(self.__sets_cells) - 1

    def go_to_the_next_state(self) -> None:
        """go_to_the_next_state"""
        if not self.has_next_state():
            raise AttributeError
        self.restore_hidden_cells()
        self.__current_index += 1
        self.__sets_cells[self.__current_index].install_all_hidden()

    def is_needed_to_solve(self) -> bool:
        """is_needed_to_solve"""

        for set_cells in self.__sets_cells:
            if set_cells.is_all_hidden():
                return False

        return True

    def restore_hidden_cells(self) -> None:
        """restore_hidden_cells"""
        for set_cells in self.__sets_cells:
            set_cells.restore()


def generate_sets_cells_wrapper(data: list[set[Cell]]) -> SetsCellsWrapper:
    """generate_sets_cells_wrapper"""
    return SetsCellsWrapper([SetCells(set_cell) for set_cell in data])
