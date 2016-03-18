from Development.LowLevelHardware.LowLevelRequest import LowLevelRequest
import time
import serial

#open port and wait for connection
port = serial.Serial("", 9600, timeout=1)
time.sleep(2)

#create request object
request = LowLevelRequest()

# or whatever this will be
objectColor = getColor()
objectDistance = getDistance()

#move forward until the robot is at the object
while objectDistance > somenumber:
    request.movement = "Forward"
    port.write(request.giveMessage())
    time.sleep(.1)
    objectDistance = getDistance()

#stop moving and lower the servo arm... wait a bit to give it time to happen
request.movement = "NoMovement"
request.servo = "Down"
port.write(request.giveMessage())
time.sleep(2)

#perform action
if objectColor == "red":
    #turn left 45 degrees
    request.wheelTurn = "Left"
    request.turnDegrees = 45
    port.write(request.giveMessage())
elif objectColor == "green":
    #turn right 45 degrees
    request.wheelTurn = "Right"
    request.turnDegrees = 45
    port.write(request.giveMessage())
elif objectColor == "purple":
    #move forward 5 times
    request.movement = "Forward"
    for i in range(0, 5):
        port.write(request.giveMessage())
elif objectColor == "yellow":
    #move backward 5 times
    request.movement = "Backward"
    for i in range(0, 5):
        port.write(request.giveMessage())
else:
    print "unidentified color"