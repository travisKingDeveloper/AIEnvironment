from Development.LowLevelHardware.LowLevelRequest import LowLevelRequest
from Development.LowLevelHardware.LowLevelResponse import LowLevelResponse
import serial
import time

#port = serial.Serial("", 9600, timeout=1)

#time.sleep(2)

request = LowLevelRequest()
response = LowLevelResponse()

request.movement = "NoMovement"
request.servo = "NoMovement"
request.wheelTurn = "NoTurn"
request.turnDegrees = "90"

print request.giveMessage()

#port.write(request.giveMessage())
#response.getMessage(port)

#print(response.isBumpedLowerLeft, response.isBumpedLowerRight, "\n")