"""Callable Interface"""

from abc import ABC, abstractmethod


class LoxCallable(ABC):
    """Abstract class for functions"""

    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass
