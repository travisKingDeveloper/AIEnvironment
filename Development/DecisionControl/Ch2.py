import LowLevelRequest
import LowLevelResponse
import time
import serial
import cv

finishTime = 30
greenTime = 45
orangeTime = 45
totalTime = 120
dropTime = 15

greenDropped = False
orangeDropped = False
droppedCount = 0

state = ""

moveDist = .2

startTime = time.clock()

#open port and wait for connection
port = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
time.sleep(2)
#set state to program 2
port.write("P3\n")

#create request object
print "creating a request object"
request = LowLevelRequest.LowLevelRequest()
response = LowLevelResponse.LowLevelResponse()

print "creating cv object"
camera = cv.CV()

def getGoal(elapsTime, curState):
    newState = ""
    multiplier = droppedCount + 1

    if elapsTime > (totalTime - finishTime):
        newState = "Find Home"
    elif greenDropped and orangeDropped:
        newState = "Find Home"
    elif greenDropped and not orangeDropped:
        newState = "Find Orange"
    elif orangeDropped and not greenDropped:
        newState = "Find Green"
    elif curState == "Find Green" and (elapsTime > (greenTime*multiplier - dropTime)):
        newState = "Drop Green"
    elif curState == "Find Orange" and (elapsTime > (orangeTime*multiplier - dropTime)):
        newState = "Drop Orange"

    return newState

def returnClosestBall(curState):
    objectList = []
    for i in range(0,6):
        if curState == "Find Green":
            objects = camera.get_green_objects()
        elif curState == "Find Orange":
            objects = camera.get_orange_objects()
        else:
            objects = camera.get_all_objects()

        for obj in objects:
            obj.append(i)
            objectList.append(obj)

        request.wheelTurn = "Right"
        request.turnDegrees = 60
        port.write(request.giveMessage())

        time.sleep(.5)

    request.wheelTurn = "NoTurn"

    distance = 1000
    for obj in objects:
        ballDist = obj[1]
        if ballDist < distance:
            distance = ballDist
            result = obj

    return result

def findDropZone(curState):
    for i in range(0, 6):
        if curState == "Drop Green":
            #look for yellow square
            #set result variable, should be facing square now, return info
            break
        elif curState == "Drop Orange":
            #look for blue quare
            #set result variable, should be facing square now, return info
            break

        request.wheelTurn = "Right"
        request.turnDegrees = 60
        port.write(request.giveMessage())
        time.sleep(.5)

    request.wheelTurn = "NoTurn"

    return result

while True:
    elapsTime = time.clock() - startTime
    state = getGoal(elapsTime, state)

    if state == "" or state == "Find Green" or state == "Find Orange":
        ball = returnClosestBall(state)

        if state == "" and ball is not None:
            if ball[0] == "green":
                state = "Find Green"
            elif ball[0] == "orange":
                state = "Find Orange"

        section = ball[ball.__sizeof__() - 1]

        for i in range(0, section):
            request.wheelTurn = "Right"
            request.turnDegrees = "60"
            port.write(request.giveMessage())
            time.sleep(.1)

        request.wheelTurn = "NoTurn"
        request.servo = "Up"
        port.write(request.giveMessage())

        ballDist = ball[1]
        wheelTurns = ballDist/moveDist

        for i in range(0, wheelTurns):
            request.movement = "Forward"
            port.write(request.giveMessage())
            time.sleep(.1)

        request.servo = "Down"
        request.movement = "NoMovement"
        port.write(request.giveMessage())

        continue

    elif state == "Drop Green" or state == "Drop Orange":
        findDropZone(state)

        #move forward to dropzone
        #   - amount to travel will either be returned by camera or camera will be constantly checked to see if its been reached
        #   - check lines
        while True:
            request.movement = "Forward"
            request.servo = "Up"
            port.write(request.giveMessage())
            time.sleep(.1)
            response.getMessage(port)

            if response.isBumpedUpperLeft and response.isBumpedUpperRight:
                request.movement = "Backward"
                request.wheelTurn = "NoTurn"
                for i in range(0, 5):
                    port.write(request.giveMessage())
                    time.sleep(.1)

                if state == "Drop Green":
                    greenDropped = True
                elif state == "Drop Orange":
                    orangeDropped = True

                droppedCount += 1

                break

            if response.isLineCenter and response.isLineLeft and response.isLineRight:
                request.wheelTurn = "NoTurn"
            elif response.isLineRight and not response.isLineLeft and response.isLineCenter:
                request.wheelTurn = "Right"
                request.turnDegrees = 3
            elif response.isLineLeft and not response.isLineRight and response.isLineCenter:
                request.wheelTurn = "Left"
                request.turnDegrees = 3
            elif response.isLineRight and not response.isLineCenter and not response.isLineLeft:
                request.wheelTurn = "Left"
                request.turnDegrees = 3
            elif response.isLineLeft and not response.isLineCenter and not response.isLineRight:
                request.wheelTurn = "Right"
                request.turnDegrees = 3

    elif state == "Find Home":
        request.wheelTurn = "Left"
        request.turnDegrees = 90
        port.write(request.giveMessage())

        time.sleep(.5)
        request.wheelTurn = "NoTurn"

        for i in range(0,5):
            request.movement = "Forward"
            port.write(request.giveMessage())
            time.sleep(.5)

        time.sleep(.5)
        request.movement = "NoMovement"

        for i in range(0,5):
            request.wheelTurn = "Right"
            request.turnDegrees = 180
            request.servo = ("Up" if request.servo == "Down" else "Up")
            port.write(request.giveMessage())
            time.sleep(.1)