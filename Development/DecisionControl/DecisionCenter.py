from Development.LowLevelHardware.LowLevelRequest import LowLevelRequest
from Development.LowLevelHardware.LowLevelResponse import LowLevelResponse
import serial
import time

port = serial.Serial("", 9600, timeout=1)

time.sleep(2)

request = LowLevelRequest()
response = LowLevelResponse()

port.write(request.giveMessage())
response.getMessage(port)

print(response.isBumpedLowerLeft, response.isBumpedLowerRight, "\n")