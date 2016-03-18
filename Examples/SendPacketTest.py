import serial
import time

#open port and give it time to connect
port = serial.Serial("COM3", 9600, timeout=1)

#this sleep is important... doesn't work without it
time.sleep(2)

#send these packets
message = "test1\ntest2\ntest3\ntest4\nblahhhhhhhhhhhhhhhh\n"

print "sending: \n" + message + ""
port.write(message)

#give the other side time to process
time.sleep(2)

print "reading..."

#while we have packets to read, read them
while port.inWaiting():
    message = port.read_until("\n")
    print message
    #give the other side time to process
    time.sleep(2)

port.close()