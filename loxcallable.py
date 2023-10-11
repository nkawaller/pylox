"""Callable Interface"""

from abc import ABC, abstractmethod
from typing import Any


class LoxCallable(ABC):
    """Abstract class for functions"""

    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter: object, arguments: list[Any]) -> float:
        pass
