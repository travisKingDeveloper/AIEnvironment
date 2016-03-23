import serial

class LowLevelResponse(object):
    def __init__(self):
        # constructor object
        self.isBumpedUpperLeft = False
        self.isBumpedUpperRight = False
        self.isBumpedLowerLeft = False
        self.isBumpedLowerRight = False
        self.isLineLeft = False
        self.isLineCenter = False
        self.isLineRight = False

    def getMessage(self, port):
        line = port.read_until("\n")

        if line[0] == "B":
            self.isBumpedUpperLeft = (True if line[1] == 1 else False)
            self.isBumpedUpperRight = (True if line[2] == 1 else False)
            self.isBumpedLowerLeft = (True if line[3] == 1 else False)
            self.isBumpedLowerRight = (True if line[4] == 1 else False)
        elif line[0] == "L":
            self.isLineLeft = (True if line[1] == 1 else False)
            self.isLineCenter = (True if line[2] == 1 else False)
            self.isLineRight = (True if line[1] == 1 else False)
