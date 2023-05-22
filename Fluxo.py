import RPi.GPIO as GPIO #Adicionar a Blibloteca RPI para as portas GPIO
import time # Adicionar a Blibloteca tempo

# Configurar os pinos GPIO
GPIO.setmode(GPIO.BCM)
OUT_PIN = 20 # Pino de saída do sensor conectado ao pino GPIO20
GPIO.setup(OUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Valor de saida do pin, gpio high, pulso positivo 

# Variáveis para cálculo do fluxo de água
pulsos = 0 # valor de pulsos 0
fluxo = 0.0 #valor de fluxo 0.0
tempo_anterior = time.time() # Valor sobre o estante do tempo

# Função de callback para a interrupção do sensor
def callback_sensor(channel):
    global pulsos
    pulsos += 1

# Configurar a interrupção no pino de saída do sensor
GPIO.add_event_detect(OUT_PIN, GPIO.FALLING, callback=callback_sensor)

# tenta
try:
    # Principal
    while True:
        # Calcular o fluxo de água a cada segundo
        tempo_atual = time.time() # Valor sobre o estante do tempo
        delta_tempo = tempo_atual - tempo_anterior # Valor de delta = sobre o estante do tempo - o tempo anterior
        tempo_anterior = tempo_atual # Tempo anterior = tempo atual

        # Calcular o fluxo de água em L/min
        fluxo = pulsos / (delta_tempo * 60) * 7.5  # 7.5 é uma constante de calibração para o sensor YF-B5

        # Imprimir o valor do fluxo de água
        print("Fluxo de água: {:.2f} L/min".format(fluxo))

        # Reiniciar a contagem de pulsos
        pulsos = 0

        # Aguardar 1 segundo
        time.sleep(1)

except KeyboardInterrupt:
    # Encerrar o programa com o pressionamento de Ctrl+C
    pass

finally:
    # Limpar a configuração dos pinos GPIO
    GPIO.cleanup()

