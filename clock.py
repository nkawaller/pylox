"""Clock native function"""


import time

import loxcallable


class Clock(loxcallable.LoxCallable):
    """Example of a native function"""

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return float(time.time())

    def __str__(self):
        return "<native fn>"
 