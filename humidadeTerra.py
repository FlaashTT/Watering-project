# Teste 1 para humidade do solo

import spidev # Adicionar a blibloteca spidev
import time # Adicionar a blibloteca tempo

# Configuração do SPI
spi = spidev.SpiDev() # Variavel = leitura do spived
spi.open(0, 0)  # Abrir o barramento SPI 0 e o dispositivo 0
spi.max_speed_hz = 1000000  # Definir a velocidade de comunicação SPI em 1MHz (opcional)

# Função para leitura do sensor de umidade do solo capacitivo
def read_capacitive_soil_moisture(channel): # Define
    # Enviar comando de leitura do canal do MCP3008
    adc = spi.xfer2([1, (8 + channel) << 4, 0]) # Ler o valor de um canal de um conversor analógico-digital (ADC)
                                                # através de uma comunicação SPI (Serial Peripheral Interface) em um microcontrolador."""
    # Interpretar resposta do MCP3008
    data = ((adc[1] & 3) << 8) + adc[2] # Extrair os dados da leitura realizada pelo conversor analógico-digital (ADC) 
                                        # através da variável adc, que contém uma lista de três valores inteiros.
                                        
    # Calcular umidade do solo baseada na resposta do sensor
    soil_moisture = (1023 - data) * 100 / 1023 # A fórmula utilizada é uma simples regra de três: a diferença entre 
                                               # 1023 (valor máximo do ADC) 
                                               # e o valor lido é dividida por 1023 e multiplicada por 100, 
                                               # para obter o percentual de umidade do solo.
    return soil_moisture # Returnar ao soil

# principal
try:
    while True:
        # Ler umidade do solo do canal 0 do MCP3008
        soil_moisture = read_capacitive_soil_moisture(0)
        # Escrever valor lido
        print(f"Umidade do solo: {soil_moisture:.2f}%")
        # Esperar 1 segundo antes da próxima leitura
        time.sleep(1)
        
except KeyboardInterrupt:
    # Encerrar programa com Ctrl+C
    spi.close()
    print("Programa encerrado.")



