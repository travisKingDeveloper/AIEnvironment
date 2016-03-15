import enum as enum

__author__ = 'travi_000'


class LowLevelRequest(object):

    def __init__(self, **kwargs):
        # Camera Degrees is 0 - 180
        # constructor object

        # If you want to go the **kwargs route
        # **kwargs is a dictionary, basically we're passing keyword arguments.
        # when constructor is called, parameters are passed like "Movement"=Movement.Forward
        # example: request = LowLevelRequest("wheelTurn"=WheelTurn.NoTurn, "Movement"=Movement.Forward)
        # or create a dictionary and pass it like so LowLevelRequest(**dict)

        self.wheelTurn = kwargs.get("WheelTurn", WheelTurn.NoTurn)
        self.movement = kwargs.get("Movement", Movement.NoMovement)
        self.servo = kwargs.get("Servo", Servo.Up)
        # self.gate = Gate
        self.degrees = kwargs.get("NumberOfDegrees", 0)
        self.wall = kwargs.get("Wall", Wall.NoMovement)
        self.CameraDegrees = kwargs.get("CameraDegrees", 0)

    def giveMessage(self):
        returnVar = ""

        if self.movement != Movement.NoMovement:
            returnVar += ("M" + "1" if self.Movement == Movement.Forward else "0" + "|")

        if self.wheelTurn != WheelTurn.NoTurn:
            returnVar += ("T" + "L" if self.wheelTurn == WheelTurn.Left else "R" + str(self.degrees) + "|")

        returnVar += ("A" + "1" if self.servo == Servo.Down else "0" + "|")

        # Commented Out For Further Use
        #returnVar += "G"
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
