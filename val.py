import time #Importar a Blibloteca Tempo
import RPi.GPIO as GPIO   # Importar a Blibloteca RPi para ler os pinos GPIO

# Definir o pin
pin = 19

# Setup da GPIO
GPIO.setmode(GPIO.BCM)    # Usar a BCM para ler as portas
GPIO.setup(pin, GPIO.OUT) # Enviar o pin para a porta de saida

# Principal
while True:
    GPIO.output(pin, GPIO.HIGH) # Ativar bomba quando tiver HIGH
    time.sleep(10)              # Esperar 10 segundos
    GPIO.output(pin, GPIO.LOW)  # Desativar a bomva quando tiver LOW
    time.sleep(2)                # Esperar 2 segundos

# Limpar as portas quando o principal acabou
GPIO.cleanup()
