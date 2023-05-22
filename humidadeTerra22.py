# teste 2 funcional

import spidev # Adicionar a Blibloteca spidev
import RPi.GPIO as GPIO # Adicionar a Blibloteca RPI acerca dos pinos gpio
import time # Adicionar a Blibloteca tempo

# Configuração do SPI
spi = spidev.SpiDev() # Variavel = leitura do SPI
spi.open(0, 0)  # Abrir o barramento SPI 0 e o dispositivo 0
spi.max_speed_hz = 1000000  # Definir a velocidade de comunicação SPI em 1MHz (opcional)

# Configuração dos pinos GPIO
FLOW_SENSOR_PIN = 20 # Ler o pin
RELAY_PIN = 13 # Ler o pin do rele

# setuo de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)

# Variáveis de controle de fluxo de água
flow_rate = 0 # Valor 0
last_pin_state = 0 # Valor 0
last_pin_change = int(time.time() * 1000) # Numero inteiro = tempo * 1000
total_water = 0 # Valor 0

# Funções para leitura do sensor de umidade do solo
def read_mcp3008(channel): 
    adc = spi.xfer2([1, (8 + channel) << 4, 0]) # Ler o valor de um canal de um conversor analógico-digital (ADC)
                                                # através de uma comunicação SPI (Serial Peripheral Interface) em um microcontrolador."""
                                                
    data = ((adc[1] & 3) << 8) + adc[2] # Extrair os dados da leitura realizada pelo conversor analógico-digital (ADC) 
                                        # através da variável adc, que contém uma lista de três valores inteiros.
    return data # returnar a data

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    # value: o valor a ser mapeado
    # in_min: o valor mínimo da faixa de entrada
    # in_max: o valor máximo da faixa de entrada
    # out_min: o valor mínimo da faixa de saída
    # out_max: o valor máximo da faixa de saída
    
# principal
try:
    while True:
        # Leitura do sensor de umidade do solo
        channel = 0  # Canal do MCP3008 a ser lido (de 0 a 7)
        value = read_mcp3008(channel)
        voltage = value * 3.3 / 1023  # Converter valor lido para tensão em Volts (3.3V é a tensão de referência do Raspberry Pi)
        soil_moisture = map_value(voltage, 0, 1.2, 0, 100)  # Mapear valor lido para porcentagem de umidade (0 a 250)
        print(f"Umidade do solo: {soil_moisture}%") # Escrever o soil

        # Controle da bomba de acordo com a umidade do solo
        if soil_moisture < 150: # Se o soil < 150
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Ligar a bomba
        else:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Desligar a bomba
    time.sleep(1) # Aguarda sempre 1 segundo
