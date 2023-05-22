import time # Importar a Blibloteca Tempo
import RPi.GPIO as GPIO   # Importar a Blibloteca RPI para a Raspbeery Pi

# Definir o PIN
pin = 13

# Set up the GPIO pin
GPIO.setmode(GPIO.BCM)    # Usa BCM para as portas gpio
GPIO.setup(pin, GPIO.OUT) # Envia o pin para a porta de saida

# Principal
while True:
    GPIO.output(pin, GPIO.HIGH) # Ligar a bomba com o determinado pin
    time.sleep(10)              # Espera 10 segundos
    GPIO.output(pin, GPIO.LOW)  # Desligar a bomba com o determinado pin
    time.sleep(2)                # Esperar 2 segundos

# Limpar a GPIO quando o principal acabar
GPIO.cleanup()
