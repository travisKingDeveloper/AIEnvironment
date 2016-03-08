import enum as enum

__author__ = 'travi_000'


class LowLevelRequest(object):

    def __init__(self , WheelTurn, NumberOfDegrees, Movement, Servo, Wall, CameraDegrees):
        # Camera Degrees is 0 - 180
        # constructor object
        self.wheelTurn = WheelTurn
        self.movement = Movement
        self.servo = Servo
        # self.gate = Gate
        self.degrees = NumberOfDegrees
        self.wall = Wall
        # camera degrees = -1 then don't turn
        self.CameraDegrees = CameraDegrees

    def giveMessage(self):
        returnVar = ""

        if self.movement != Movement.NoMovement:
            returnVar += ("M" + "1" if self.Movement == Movement.Forward else "0" + "|")

        if self.wheelTurn != WheelTurn.NoTurn:
            returnVar += ("T" + "L" if self.wheelTurn == WheelTurn.Left else "R" + str(self.degrees) + "|")

        returnVar += ("A" + "1" if self.servo == Servo.Down else "0" + "|")
        returnVar += "G"

        # Commented Out For Further Use
        # if self.gate == Gate.Left:
        #     returnVar += "10|"
        # elif self.gate == Gate.Right:
        #     returnVar += "01|"
        # else:
        #     returnVar += "00|"

        if self.wall != Wall.NoMovement:
            returnVar += "W"
            if self.wall == Wall.Close:
                returnVar += "C|"
            elif self.wall == Wall.Left:
                returnVar += "L|"
            else:
                returnVar += "R|"

        if self.CameraDegrees != -1:
            returnVar += "C" + str(self.CameraDegrees)

        return returnVar

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


class Wall(enum):
    Left = 1
    Right = 2
    NoMovement = 0
    Close = 3

# class Gate(enum):
#     Left = 10
#     Right = 01
#     Blocked = 00
