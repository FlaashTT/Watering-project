import time
import math
import Adafruit_ADS1x15 # Library for ADS1x15 ADC chip

ANALOG_PIN = 16
RANGE = 5000 # Depth measuring range 5000mm (for water)
VREF = 5000 # ADC's reference voltage on your Arduino,typical value:5000mV
CURRENT_INIT = 4.00 # Current @ 0mm (uint: mA)
DENSITY_WATER = 1  # Pure water density normalized to 1
DENSITY_GASOLINE = 0.74  # Gasoline density
PRINT_INTERVAL = 1

adc = Adafruit_ADS1x15.ADS1115() # Create an ADS1115 ADC (16-bit) instance

def read_analog():
    # Read the ADC value from selected pin (ANALOG_PIN) in single-ended mode
    value = adc.read_adc(ANALOG_PIN, gain=1, data_rate=860)
    voltage = (value / 32767.0) * VREF # Calculate the voltage
    return voltage

def main():
    while True:
        start_time = time.monotonic()
        dataVoltage = read_analog()
        dataCurrent = dataVoltage / 120.0 # Sense Resistor: 120ohm
        depth = (dataCurrent - CURRENT_INIT) * (RANGE / DENSITY_WATER / 16.0) # Calculate depth from current readings

        if depth < 0:
            depth = 0.0

        # Print results
        print(f"depth: {depth:.2f} mm")

        elapsed_time = time.monotonic() - start_time
        time.sleep(max(PRINT_INTERVAL - elapsed_time, 0))

if __name__ == '__main__':
    main()
import time
import math
import Adafruit_ADS1x15 # Library for ADS1x15 ADC chip

ANALOG_PIN = 2
RANGE = 5000 # Depth measuring range 5000mm (for water)
VREF = 5000 # ADC's reference voltage on your Arduino,typical value:5000mV
CURRENT_INIT = 4.00 # Current @ 0mm (uint: mA)
DENSITY_WATER = 1  # Pure water density normalized to 1
DENSITY_GASOLINE = 0.74  # Gasoline density
PRINT_INTERVAL = 1

adc = Adafruit_ADS1x15.ADS1115() # Create an ADS1115 ADC (16-bit) instance

def read_analog():
    # Read the ADC value from selected pin (ANALOG_PIN) in single-ended mode
    value = adc.read_adc(ANALOG_PIN, gain=1, data_rate=860)
    voltage = (value / 32767.0) * VREF # Calculate the voltage
    return voltage

def main():
    while True:
        start_time = time.monotonic()
        dataVoltage = read_analog()
        dataCurrent = dataVoltage / 120.0 # Sense Resistor: 120ohm
        depth = (dataCurrent - CURRENT_INIT) * (RANGE / DENSITY_WATER / 16.0) # Calculate depth from current readings

        if depth < 0:
            depth = 0.0

        # Print results
        print(f"depth: {depth:.2f} mm")

        elapsed_time = time.monotonic() - start_time
        time.sleep(max(PRINT_INTERVAL - elapsed_time, 0))

if __name__ == '__main__':
    main()
