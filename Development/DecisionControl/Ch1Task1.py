import time
import serial

#open port and give it time to connect
port = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
time.sleep(2)

#send command to start challenge 1 task 1 and close
port.write("P1\n")

port.in_waiting

while True:
    if port.read_until("\n") == "P0":
        print "Task completed"
    time.sleep(2)

port.close()
