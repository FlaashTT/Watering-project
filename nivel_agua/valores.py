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
    current = voltage / 141000.0 # Sense Resistor:120ohm
    return current

def main():
    while True:
        voltage = read_voltage()
        current = calculate_current(voltage)
        print("voltage: {}mV, current: {}mA".format(voltage, current))
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
