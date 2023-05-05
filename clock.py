"""Clock native function"""


import loxcallable
import time

class Clock(loxcallable.LoxCallable):

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return float(time.time())

    def __str__(self):
        return "<native fn>"