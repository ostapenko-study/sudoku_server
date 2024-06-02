"""solution module"""
from typing import TypeAlias

from sudoku_package.cell import Cell, CellListener
from sudoku_package.cell_with_sets_cells_wrapper import (CellWithSetsCellsWrapper,
                                                         generate_cell_with_sets_cells_wrapper)
from sudoku_package.storage import Storage
from sudoku_package.iset import ISet

IndexContainer: TypeAlias = set[int]


class Solver(CellListener):
    """solution class"""

    def __init__(self, storage: Storage, checker: ISet):
        self.__storage = storage
        self.__checker = checker
        self.__hidden_indexes = IndexContainer()
        self.__sets = None
        self.__set_map_stack = list[CellWithSetsCellsWrapper]()

        for cell in self.__storage.cells():
            cell.add_listener(self)

        self.__hidden_indexes_list = []

    def on_cell_hidden_changed(self, cell) -> None:
        index = self.__storage.index_by_cell(cell)
        if cell.is_hidden():
            self.__hidden_indexes.add(index)
            self.__hidden_indexes_list.append(index)
        else:
            self.__hidden_indexes.remove(index)
            self.__hidden_indexes_list.remove(index)

    def __find_next_set_map_by_up(self) -> bool:
        new_index = self.__sets.index(self.__set_map_stack[-1].to_data())
        new_index += 1
        while new_index != len(self.__sets):
            sets_cells_wrapper = generate_cell_with_sets_cells_wrapper(self.__sets[new_index])
            if sets_cells_wrapper.is_needed_to_solve():
                self.__set_map_stack.append(sets_cells_wrapper)
                return True
            new_index += 1
        return False

    def __find_next_set_map_by_down(self) -> bool:
        while len(self.__set_map_stack) != 0:
            if self.__set_map_stack[-1].has_next_state():
                return True
            self.__set_map_stack[-1].restore_hidden_cells()
            self.__set_map_stack.pop()
        return False

    def solve(self) -> list[int]:
        """ solution method"""

        self.__sets = self.__create_hidden_interesting_cell_sets()

        if len(self.__sets) == 0:
            return []

        self.__set_map_stack = [generate_cell_with_sets_cells_wrapper(self.__sets[0])]

        while len(self.__set_map_stack) != 0:
            status = False
            while self.__set_map_stack[-1].has_next_state():
                self.__set_map_stack[-1].go_to_the_next_state()
                if self.__check_combination():
                    if not self.__find_next_set_map_by_up():
                        status = True
                        break

            if status:
                break

            self.__find_next_set_map_by_down()
        return sorted(self.__hidden_indexes)

    def __create_hidden_interesting_cell_sets(self) -> list[tuple[Cell, list[set[Cell]]]]:
        answer = []

        for cell in self.__storage.cells():
            not_compatibility_cells = self.__checker.get_not_compatibility_sets_cells(cell)
            if len(not_compatibility_cells):
                answer.append((cell, not_compatibility_cells))

        return answer

    def check_combination(self) -> bool:
        """public method of checking combination"""
        return self.__check_combination()

    def __check_combination(self) -> bool:
        if not self.__check_hidden_cells():
            return False
        if not self.__check_not_hidden_cells():
            return False

        return True

    def __check_neighbor_by_index(self, index: int, is_hidden: bool) -> bool:
        return self.__storage.cells()[index].is_hidden() == is_hidden

    def __check_neighbor_by_pair(self, _x: int, _y: int, is_hidden: bool) -> bool:
        return self.__check_neighbor_by_index(self.__storage.index_from_xy(_x, _y), is_hidden)

    def __get_neighbors(self, index: int) -> list[tuple[int, int]]:
        _x, _y = self.__storage.index_to_xy(index)
        answer_pairs = []
        if _x > 0:
            answer_pairs.append((_x - 1, _y))
        if _x < self.__storage.col_count() - 1:
            answer_pairs.append((_x + 1, _y))
        if _y > 0:
            answer_pairs.append((_x, _y - 1))
        if _y < self.__storage.row_count() - 1:
            answer_pairs.append((_x, _y + 1))
        return answer_pairs

    def __is_cell_has_neighbor(self, index: int, is_hidden: bool) -> bool:
        for x_y in self.__get_neighbors(index):
            if self.__check_neighbor_by_pair(x_y[0], x_y[1], is_hidden):
                return True
        return False

    def __check_hidden_cells(self):
        for index in self.__hidden_indexes:
            if self.__is_cell_has_neighbor(index, True):
                return False

        return True

    def __create_not_hidden_indexes(self) -> IndexContainer:
        answer = IndexContainer()
        for i in range(len(self.__storage.cells())):
            if i not in self.__hidden_indexes:
                answer.add(i)
        return answer

    def __check_not_hidden_cells(self):
        not_hidden_indexes = self.__create_not_hidden_indexes()
        if len(not_hidden_indexes) == 0:
            return True
        first_index = next(iter(not_hidden_indexes))
        visited = set[int]()
        order = list[int]([first_index])
        while len(visited) != len(not_hidden_indexes):
            if len(order) == 0:
                return False
            current_index = order.pop()
            visited.add(current_index)
            neighbors = [
                self.__storage.index_from_xy(p[0], p[1])
                for p in self.__get_neighbors(current_index)
            ]
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                if self.__check_neighbor_by_index(neighbor, False):
                    order.append(neighbor)

        return True
