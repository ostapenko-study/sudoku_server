"""
task generator

csvfile from
https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings
"""
import csv
import math
import random
import orm_sqlite

DATABASE_FILE = "sudoku_package/data.db"


def str_to_array(data):
    """str to array"""
    return [int(letter) for letter in data]


class Task(orm_sqlite.Model):
    """!!!"""
    id = orm_sqlite.IntegerField(primary_key=True)
    numbers = orm_sqlite.StringField()
    # row_count = orm_sqlite.IntegerField()
    # col_count = orm_sqlite.IntegerField()

    objects = None  # E1101


#
# class HiddenIndexes(orm_sqlite.Model):
#     id = orm_sqlite.IntegerField(primary_key=True)
#     indexes = orm_sqlite.StringField()


class Database:
    """!!!"""

    def __init__(self, db_file):
        """!!!"""
        self.__db = orm_sqlite.Database(db_file)
        Task.objects.backend = self.__db

    def add(self, task: dict):
        """!!!"""
        Task.objects.add(task)

    def create(self, csv_source_file):
        """!!!"""
        Task.drop()
        Task.create()
        with open(csv_source_file, 'r', encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                self.add({
                    'task': row[2],
                    # 'row_count': 9,
                    # 'col_count': 9
                })

    def get_by_id(self, id_value):
        """!!!"""
        sudoku = self.get_sudoku_by_id(id_value)
        block_size = int(math.sqrt(len(sudoku)))
        hidden_indexes = self.generate_hidden_indexes(id_value, block_size)
        for index in hidden_indexes:
            sudoku[index] = random.randint(1, block_size)
        return sudoku

    def get_sudoku_by_id(self, id_value):
        """!!!"""
        min_max_result = self.__db.select("select min(id) as minId, max(id) as maxId from task")[0]
        min_id, max_id = min_max_result["minId"], min_max_result["maxId"]
        id_value = id_value % (max_id - min_id + 1) + min_id
        task = Task.objects.get(pk=id_value)
        return str_to_array(task["numbers"])

    def check_borders(self, value, d_value, m):
        """!!!"""
        if value == 0 and d_value == -1:
            return False
        if value == m - 1 and d_value == 1:
            return False
        return True

    def generate_hidden_indexes(self, id_value, block_size):
        """!!!"""
        # count_of_indexes = id_value % block_size + 2
        count_of_indexes = 5
        answer = []
        numbers = list(range(block_size ** 2))
        d_var_array = [-1, 0, 1]
        for _ in range(count_of_indexes):
            index = random.choice(numbers)
            answer.append(index)
            numbers.remove(index)
            current_x = index % block_size
            current_y = index // block_size
            for dx in d_var_array:
                if not self.check_borders(current_x, dx, block_size):
                    continue

                for dy in d_var_array:
                    if not self.check_borders(current_y, dy, block_size):
                        continue
                    new_index = (current_y + dy) * block_size + current_x + dx
                    if new_index in numbers:
                        numbers.remove(new_index)

        return answer


def task_generator(id_value: int):
    """task_generator"""
    __db = Database(DATABASE_FILE)
    return {
        "cols": 9,
        "rows": 9,
        "numbers": __db.get_by_id(id_value)
    }


# if __name__ == "__main__":
#     db = Database(DATABASE_FILE)
#     db.create(CSV_SUDOKU_FILE)
