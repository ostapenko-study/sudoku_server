"""!!!"""
from abc import ABC, abstractmethod


class CellListener(ABC):
    """!!!"""
    @abstractmethod
    def on_cell_hidden_changed(self, cell) -> None:
        """!!!"""

    def __str__(self):
        return self.__class__.__name__


class Cell:
    """!!!"""

    def __init__(self, value):
        self.__value = value
        self.__hidden = False
        self.__listeners = list[CellListener]()

    def add_listener(self, listener: CellListener):
        """!!!"""
        self.__listeners += [listener]

    def value(self):
        """!!!"""
        return self.__value

    def set_hidden(self, state: bool):
        """!!!"""
        if self.__hidden == state:
            return
        self.__hidden = state
        for listener in self.__listeners:
            listener.on_cell_hidden_changed(self)

    def is_hidden(self):
        """!!!"""
        return self.__hidden

    def __str__(self):
        """!!!"""
        if self.__hidden:
            return f'({self.__value})'
        return f' {self.__value} '
