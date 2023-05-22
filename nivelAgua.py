#Este codigo mostra a profundidade em cm do sensor de nivel de água
#Testado e funciona

import RPi.GPIO as GPIO # Adiconar as bliblotecas do RPI pelas portas do GPIO
import time # Adcionar as bliblotecas tempo

CurrentSensorPin = 23
VREF = 3300 # ADC's voltagem de referencia do proprio current to voltage, value:5000mV

# Setup das portas gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(CurrentSensorPin, GPIO.IN)


def read_voltage():
    # Lê o valor digital do pino do sensor e convertendo para tensão em volts
    voltage = (GPIO.input(CurrentSensorPin) * 3.3 / 1024) * VREF
    return voltage

def calculate_current(voltage):
    current = voltage / 120.0 # Usa o valor da tensão medida e o valor da resistência do sensor para calcular a corrente elétrica
    return current

def main():
    while True:
        # Calculando a corrente elétrica medida pelo sensor
        voltage = read_voltage() * VREF / 1024.0
        # Corrente = voltagem do sensor / pela resistencia
        current = voltage / 120.0
        # Convertendo a corrente elétrica em profundidade da água em centímetros
        depth = (4.00 - current) * (50 / 1 / 16.0)
        # Arredonda o valor para duas casas decimais
        rounded = round(depth, 2)
        # Exibindo no terminal a corrente elétrica, a tensão e a profundidade calculada
        print("profundidade: {}cm".format(rounded))
        time.sleep(2)


# Inicia o programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
