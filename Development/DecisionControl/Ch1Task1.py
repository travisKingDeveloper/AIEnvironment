import time
import serial

#open port and give it time to connect
port = serial.Serial("", 9600, timeout=1)
time.sleep(2)

#send command to start challenge 1 task 1 and close
port.write("C1T1\n")
port.close()
