"""test module"""
import random

from sudoku_package.checker_generators import generate_sudoku_checker, generate_main_checkers
from sudoku_package.checkers import generate_mini_checker, DisjunctionChecker
from sudoku_package.data import correct_sudoku_list
from sudoku_package.solver import Solver
from sudoku_package.storage import Storage
from sudoku_package.block import Block
from sudoku_package.cell import Cell
from sudoku_package.task_generator import task_generator

N = 5


def test_global():
    for _ in range(N):
        task = task_generator(random.randint(1, 999999))
        st = Storage(task["numbers"])
        st.set_shape(task["rows"], task["cols"])
        checker = generate_sudoku_checker(st, block_size=3)
        solver = Solver(st, checker)
        result = solver.solve()
        assert result
        assert checker.is_correct()


def test_storage_shape():
    """storage_shape"""
    data = []
    for _ in range(N):
        data.append((random.randint(3, 15), random.randint(3, 15),))

    for row, col in data:
        st = Storage([])
        st.set_shape(row, col)
        assert st.col_count() == col
        assert st.row_count() == row


def test_storage_indexes():
    """storage_indexes"""
    st = Storage([
        1, 2, 3, 4, 5, 6,
        5, 4, 2, 3, 1, 7,
        8, 3, 4, 1, 6, 3,
        6, 2, 3, 7, 5, 2,
        9, 6, 3, 6, 4, 2,
        7, 3, 5, 2, 7, 4,
    ])
    st.set_shape(6, 6)
    for index, (x, y) in [
        (5, (5, 0)),
        (2, (2, 0)),
        (7, (1, 1)),
        (9, (3, 1)),
        (35, (5, 5)),
        (17, (5, 2)),
    ]:
        assert st.index_to_xy(index) == (x, y)
        assert index == st.index_from_xy(x, y)


def test_clear_storage():
    """clear_storage"""
    st = Storage([
        1, 2, 3, 4, 5, 6,
        5, 4, 2, 3, 1, 7,
        8, 3, 4, 1, 6, 3,
        6, 2, 3, 7, 5, 2,
        9, 6, 3, 6, 4, 2,
        7, 3, 5, 2, 7, 4,
    ])
    for _ in range(N):
        random.choice(st.cells()).set_hidden(False)

    st.clear()
    for cell in st.cells():
        assert not cell.is_hidden()


def test_print_storage():
    """print_storage"""
    st = Storage([
        1, 2,
        5, 4,
    ])
    st.set_shape(2, 2)
    st.at(1, 1).set_hidden(True)
    st.at(0, 1).set_hidden(True)
    st.at(1, 0).set_hidden(True)
    assert str(st) == " 1 \t(2)\t\n(5)\t(4)\t\n"


def test_block_cells():
    """block_cells"""
    cell_list = []
    for i in range(N):
        cell_list.append(Cell(i))

    block = Block(cell_list)
    for i in range(N // 2):
        cell = random.choice(cell_list)
        cell.set_hidden(False)
        assert str(cell) == f' {cell.value()} '
        assert block.is_correct()
        assert block.has_cell(cell)

    for i in range(N // 2):
        cell = random.choice(cell_list)
        cell.set_hidden(True)
        assert str(cell) == f'({cell.value()})'
        assert block.is_correct()
        assert block.has_cell(cell)

    for i in range(N // 4):
        assert not block.has_cell(Cell(i))


def test_block_get_not_compatibility_sets_cells():
    """block_get_not_compatibility_sets_cells"""
    cell_list = []
    for i in range(N):
        cell_list.append(Cell(i))
        cell_list.append(Cell(i))

    block = Block(cell_list)
    assert not block.is_correct()

    for i in range(N):
        first, second = cell_list[i * 2], cell_list[i * 2 + 1]
        assert block.get_not_compatibility_sets_cells(first) == [{second}]
        assert block.get_not_compatibility_sets_cells(second) == [{first}]

    for i in range(N):
        assert block.get_not_compatibility_sets_cells(Cell(i)) == [set()]


def test_sudoku_checker():
    """sudoku_checker"""
    for correct_sudoku in correct_sudoku_list:
        st = Storage(correct_sudoku)
        st.set_shape(9, 9)
        checker = generate_sudoku_checker(st)
        assert checker.is_correct()
        for _ in range(N):
            cell = random.choice(st.cells())
            assert checker.get_not_compatibility_sets_cells(cell) == []


def test_invalid_storage_for_checkers():
    """invalid_storage_for_checkers"""
    st = Storage([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    for x_value, y_value in [
        (3, 4),
        (4, 3),
        (4, 4)
    ]:
        st.set_shape(x_value, y_value)
        try:
            generate_mini_checker(st)
            assert False
        except AttributeError:
            assert True


def test_disjunction_checker():
    """disjunction_checker"""
    common_cells = []
    cells1 = []
    cells2 = []
    for i in [1, 2, 3]:
        cell = Cell(i)
        common_cells.append(cell)
        cells1.append(cell)
        cells2.append(cell)

    for i in [1, 2, 4, 7, 9, 5, 5, 1]:
        cells1.append(Cell(i))
    block1 = Block(cells1)

    for i in [1, 4, 4, 7, 7, 1, 5, 1]:
        cells2.append(Cell(i))
    block2 = Block(cells2)
    disjunction_checker = DisjunctionChecker([block1, block2])
    assert not disjunction_checker.is_correct()
    assert not disjunction_checker.get_not_compatibility_sets_cells(common_cells[2])
    assert not disjunction_checker.get_not_compatibility_sets_cells(cells1[5])
    assert not disjunction_checker.get_not_compatibility_sets_cells(cells2[4])
