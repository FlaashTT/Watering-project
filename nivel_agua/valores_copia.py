#Este codigo mostra a profundidade em cm do sensor de nivel de água
#Testado e funciona

import RPi.GPIO as GPIO
import time

CurrentSensorPin = 23
VREF = 3300 # ADC's reference voltage on your Arduino,typical value:5000mV

GPIO.setmode(GPIO.BCM)
GPIO.setup(CurrentSensorPin, GPIO.IN)

def read_voltage():
    voltage = (GPIO.input(CurrentSensorPin) * 3.3 / 1024) * VREF
    return voltage

def calculate_current(voltage):
    current = voltage / 120.0 # Sense Resistor:120ohm
    return current

def main():
    while True:
        voltage = read_voltage() * VREF / 1024.0
        current = voltage / 120.0
        depth = (4.00 - current) * (50 / 1 / 16.0)
        rounded = round(depth, 2)
        print("profundidade: {}cm".format(rounded))
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
