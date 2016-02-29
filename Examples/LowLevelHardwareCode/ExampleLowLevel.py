__author__ = 'travi_000'


def function_low_level():
    print("This is an example of low level calls")
    # remember that you indent to define functions


class LowLevel(object):
    def turn_wheel(self, amount):
        # example of a function you might make
        return amount

    def __init__(self):
        # constructor object
        self.wheelDegrees = 0

    def add_degree(self, amount):
        # another example
        self.wheelDegrees = (amount + self.wheelDegrees) % 360

        self.turn_wheel(self.wheelDegrees)

        return amount
