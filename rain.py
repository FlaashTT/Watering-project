import RPi.GPIO as GPIO # Adicionar a blibloteca RPI com as portas gpio
import time # Adicionar a blibloteca tempo

GPIO.setmode(GPIO.BCM) # Leitura do gpio na placa

# Configuração do pino do sensor de chuva
RAIN_SENSOR_PIN = 16 # Ler o pin
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN) # Leitura da placa sobre o pin lido
# principal
while True:
    # Leitura do valor do sensor de chuva
    if GPIO.input(RAIN_SENSOR_PIN) == GPIO.HIGH: # Quando tiver high
        print("Sem chuva") # Escreve sem chuva
    else: # senao
        print("Chuva detectada") # Escreve com chuva
    
    time.sleep(1) # aguarda 1 segundo antes de ler novamente
