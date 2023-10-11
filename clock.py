"""Clock native function"""


import time
from loxcallable import LoxCallable
from typing import Any


class Clock(LoxCallable):
    """Example of a native function"""

    def arity(self) -> int:
        return 0

    def call(self, interpreter: object, arguments: list[Any]) -> float:
        return float(time.time())

    def __str__(self) -> str:
        return "<native fn>"
