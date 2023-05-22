import serial
import RPi.GPIO as GPIO     
import os, time

GPIO.setmode(GPIO.BOARD)   

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
port = serial.Serial("COM22", baudrate=9600, timeout=1)

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

port.write(b'AT'+'\r\n')
rcv = port.read(10)
print (rcv)
time.sleep(1)


