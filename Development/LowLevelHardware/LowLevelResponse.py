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

        for packet in packetList:
            if packet[0] == "B":
                self.isBumpedUpperLeft = (True if packet[1] == 1 else False)
                self.isBumpedUpperRight = (True if packet[2] == 1 else False)
                self.isBumpedLowerLeft = (True if packet[3] == 1 else False)
                self.isBumpedLowerRight = (True if packet[4] == 1 else False)
            elif packet[0] == "L":
                self.isLineLeft = (True if packet[1] == 1 else False)
                self.isLineCenter = (True if packet[2] == 1 else False)
                self.isLineRight = (True if packet[1] == 1 else False)
