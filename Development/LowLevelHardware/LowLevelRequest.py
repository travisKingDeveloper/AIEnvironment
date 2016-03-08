import enum as enum

__author__ = 'travi_000'


class LowLevelRequest(object):
    def __init__(self , WheelTurn, NumberOfDegrees, Movement, Servo, Gate):
        # constructor object
        self.wheelTurn = WheelTurn
        self.movement = Movement
        self.servo = Servo
        self.gate = Gate
        self.degrees = NumberOfDegrees

    def giveMessage(self):
        returnVar = ""

        if self.movement != Movement.NoMovement:
            returnVar += ("M" + "1" if self.Movement == Movement.Forward else "0" + "|")

        if self.wheelTurn != WheelTurn.NoTurn:
            returnVar += ("T" + "L" if self.wheelTurn == WheelTurn.Left else "R" + str(self.degrees) + "|")

        returnVar += ("A" + "1" if self.servo == Servo.Down else "0" + "|")
        returnVar += "G"



class WheelTurn(enum):
    Left = 1
    Right = 2
    NoTurn = 3


class Movement(enum):
    Forward = 1
    Backward = 2
    NoMovement = 3


class Servo(enum):
    Up = 0
    Down = 1


class Gate(enum):
    Left = 10
    Right = 01
    Blocked = 00
