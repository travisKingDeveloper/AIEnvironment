import LowLevelRequest
import LowLevelResponse
import time
import serial
import cv

#timer variables
finishTime = 30
greenTime = 45
orangeTime = 45
totalTime = 120
dropTime = 15

#state variables
greenDropped = False
orangeDropped = False
droppedCount = 0

state = ""

#the amount of distance travelled by one M1 command
moveDist = .2

startTime = time.clock()

#open port and wait for connection
port = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
time.sleep(2)
#set state to program 2
port.write("P3\n")

#create responce and request object
print "creating a request object"
request = LowLevelRequest.LowLevelRequest()
response = LowLevelResponse.LowLevelResponse()

#create camera object
print "creating cv object"
camera = cv.CV()

#decide on the next state based on variables
def getGoal(elapsTime, curState):
    newState = ""
    multiplier = droppedCount + 1
    #multiplier increments when a color has been collected and dropped off
    #indicates which run we're on, and the maximum ellapsed time we can have

    # 90 seconds ellapsed, go home
    if elapsTime > (totalTime - finishTime):
        newState = "Find Home"
    #green dropped and orange dropped, go home
    elif greenDropped and orangeDropped:
        newState = "Find Home"
    #green dropped and orange hasn't been dropped, collect orange
    elif greenDropped and not orangeDropped:
        newState = "Find Orange"
    #orange dropped and green hasn't been dropped, collect green
    elif orangeDropped and not greenDropped:
        newState = "Find Green"
    #currently finding green and the 30 second time to collect has passed, drop green off
    elif curState == "Find Green" and (elapsTime > (greenTime*multiplier - dropTime)):
        newState = "Drop Green"
    #currently finding orange and the 30 second time to collect has passed, drop orange off
    elif curState == "Find Orange" and (elapsTime > (orangeTime*multiplier - dropTime)):
        newState = "Drop Orange"

    return newState

#return the closest ball
def returnClosestBall(curState):
    objectList = []
    #rotate 6 times, 60 degrees each time, and collect all objects the camera sees
    for i in range(0,6):
        if curState == "Find Green":
            objects = camera.get_green_objects()
        elif curState == "Find Orange":
            objects = camera.get_orange_objects()
        else:
            objects = camera.get_all_objects()

        #append which turn each object was observed at, then add object to list
        for obj in objects:
            obj.append(i)
            objectList.append(obj)

        #rotate 60 degrees
        request.wheelTurn = "Right"
        request.turnDegrees = 60
        port.write(request.giveMessage())

        #give low level enough time to process and execute
        time.sleep(.5)

    #set turn back to NoTurn
    request.wheelTurn = "NoTurn"

    #find the closest ball in the list
    distance = 1000
    for obj in objects:
        ballDist = obj[1]
        if ballDist < distance:
            distance = ballDist
            result = obj

    #return closest ball
    return result

def findDropZone(curState):
    #rotate 6 times, 60 degrees each time, stop when we see the goal square
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

    #set turn back to NoTurn
    request.wheelTurn = "NoTurn"

    return result

while True:
    #calculate ellapsed time
    elapsTime = time.clock() - startTime
    #get next state
    state = getGoal(elapsTime, state)

    #if no state(initial condition) or Find
    if state == "" or state == "Find Green" or state == "Find Orange":
        ball = returnClosestBall(state)

        #if state is empty and a ball was found, start collecting that color
        if state == "" and ball is not None:
            if ball[0] == "green":
                state = "Find Green"
            elif ball[0] == "orange":
                state = "Find Orange"

        #get which section in the 60 degree turn of returnClosestBall() the closest ball is in
        section = ball[ball.__sizeof__() - 1]

        #rotate back to that section
        for i in range(0, section):
            request.wheelTurn = "Right"
            request.turnDegrees = "60"
            port.write(request.giveMessage())
            time.sleep(.1)

        #stop turning and move arm up
        request.wheelTurn = "NoTurn"
        request.servo = "Up"
        port.write(request.giveMessage())

        #calculate how many times M1 needs to be sent
        ballDist = ball[1]
        wheelTurns = ballDist/moveDist

        #send M1 packets
        for i in range(0, wheelTurns):
            request.movement = "Forward"
            port.write(request.giveMessage())
            time.sleep(.1)

        #stop and move arm down
        request.servo = "Down"
        request.movement = "NoMovement"
        port.write(request.giveMessage())

        continue

    elif state == "Drop Green" or state == "Drop Orange":
        #orientate robot to the dropzone
        findDropZone(state)

        #move forward to dropzone
        #   - amount to travel will either be returned by camera or camera will be constantly checked to see if its been reached
        #   - once black line reached, follow it
        #   - once bumpers have been activated, reverse and dump balls
        while True:
            #move forward and move arm up
            request.movement = "Forward"
            request.servo = "Up"
            port.write(request.giveMessage())
            time.sleep(.1)
            #read response from
            response.getMessage(port)

            #if bumpers are hit, dump balls
            if response.isBumpedUpperLeft and response.isBumpedUpperRight:
                request.movement = "Backward"
                request.wheelTurn = "NoTurn"
                for i in range(0, 5):
                    port.write(request.giveMessage())
                    time.sleep(.1)

                #update variables
                if state == "Drop Green":
                    greenDropped = True
                elif state == "Drop Orange":
                    orangeDropped = True

                droppedCount += 1

                break

            #line following
            #if all 3 lines are black, move forward
            if response.isLineCenter and response.isLineLeft and response.isLineRight:
                request.wheelTurn = "NoTurn"
            #Center, Right, are black. Left is white. Turn right.
            elif response.isLineRight and not response.isLineLeft and response.isLineCenter:
                request.wheelTurn = "Right"
                request.turnDegrees = 3
            #Center, Left, are black. Right is white. Turn left.
            elif response.isLineLeft and not response.isLineRight and response.isLineCenter:
                request.wheelTurn = "Left"
                request.turnDegrees = 3
            #Right is black. Center and Left are white. Turn left.
            elif response.isLineRight and not response.isLineCenter and not response.isLineLeft:
                request.wheelTurn = "Left"
                request.turnDegrees = 3
            #Left is black. Center and Right are white. Turn right.
            elif response.isLineLeft and not response.isLineCenter and not response.isLineRight:
                request.wheelTurn = "Right"
                request.turnDegrees = 3

        continue

    # THIS ONLY WORKS IF WE ARE DUMPING WAS THE LAST STATE
    # Turn 90 degrees and go forward some amount, however far home would be
    # afterwards, dance.
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

        # DANCE!!!!!!!!
        for i in range(0,5):
            request.wheelTurn = "Right"
            request.turnDegrees = 180
            request.servo = ("Up" if request.servo == "Down" else "Up")
            port.write(request.giveMessage())
            time.sleep(.1)

        continue