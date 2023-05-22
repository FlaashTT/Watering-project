import spidev
import RPi.GPIO as GPIO
import time
import sys
import datetime
import serial

#GSM
ser = serial.Serial("/dev/ttyS0",115200)  # Define a porta serial utilizada para se comunicar com o módulo SIM7600X e a taxa de transmissão
ser.flushInput()  # Limpa o buffer de entrada da porta serial
now = datetime.datetime.now()
phone_number = '+351'  # Número de telefone para onde serão enviadas as mensagens
text_message1 = 'Valor de Humidade: {}'.format(soil_moisture)
# text_message1 = ('Valor de Humidade:',soil_moisture)
# text_message = 'Com chuva!'  
power_key = 6  # Define o pino GPIO que será utilizado para ligar/desligar o módulo SIM7600X
rec_buff = ''  # Buffer para armazenar as respostas do módulo SIM7600X

# Configuração do SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Abrir o barramento SPI 0 e o dispositivo 0
spi.max_speed_hz = 1000000  # Definir a velocidade de comunicação SPI em 1MHz (opcional)


#Nivel
VREF = 3300
#Fluxo
pulsos = 0
fluxo = 0.0
tempo_anterior = time.time()

# Configuração da bomba e do sensor de fluxo de água
OUT_PIN = 20
RELAY_PIN = 13
RAIN_DROP_PIN = 16
VALVE_PIN = 19
CurrentSensorPin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CurrentSensorPin, GPIO.IN)
GPIO.setup(RAIN_DROP_PIN, GPIO.IN)
GPIO.setup(VALVE_PIN, GPIO.OUT)
GPIO.setup(VALVE_PIN, GPIO.LOW)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

def send_at(command,back,timeout):
	rec_buff = ''  # Limpa o buffer de resposta
	ser.write((command+'\r\n').encode())  # Envia o comando pela porta serial
	time.sleep(timeout)  # Aguarda o tempo definido
	if ser.inWaiting():  # Se houver dados disponíveis na porta serial
		time.sleep(0.01 )
		rec_buff = ser.read(ser.inWaiting())  # Lê os dados da porta serial e armazena no buffer de resposta
	if back not in rec_buff.decode():  # Se a resposta esperada não estiver contida no buffer de resposta
		print(command + ' ERROR')  # Imprime a mensagem de erro
		print(command + ' back:\t' + rec_buff.decode())
		return 0  # Retorna 0 indicando que houve erro
	else:
		print(rec_buff.decode())  # Imprime a resposta recebida
		return 1  # Retorna 1 indicando que tudo ocorreu corretamente

def SendShortMessage(phone_number,text_message):
	
	print("Setting SMS mode...")  # Imprime a mensagem de configuração do modo SMS
	send_at("AT+CMGF=1","OK",1)  # Configura o modo SMS
	print("Sending Short Message")  # Imprime a mensagem de envio da mensagem
	answer = send_at("AT+CMGS=\""+phone_number+"\"",">",2)  # Envia o comando para enviar a mensagem
	if 1 == answer:
		ser.write(text_message.encode())  # Envia a mensagem pela porta serial
		ser.write(b'\x1A')  # Envia o caractere de fim de mensagem
		answer = send_at('','OK',20)  # Aguarda a resposta confirmando o envio da mensagem
		if 1 == answer:
			print('send successfully')  # Imprime a mensagem de sucesso no envio da mensagem
		else:
			print('error')  # Imprime a mensagem de erro
	else:
		print('error%d'%answer)

def ReceiveShortMessage():
	rec_buff = ''
	print('Setting SMS mode...') # Imprime a mensagem de configuração do modo SMS
	send_at('AT+CMGF=1','OK',1) # Configura o modo SMS
	send_at('AT+CPMS=\"SM\",\"SM\",\"SM\"', 'OK', 1) # Configura o modo SMS
	answer = send_at('AT+CMGR=1','+CMGR:',2) # Envia o comando para enviar a mensagem do statu do gms
	if 1 == answer:
		answer = 0
		if 'OK' in rec_buff: # Se der ok em buffer vai enviar um valor (1)
			answer = 1 
			print(rec_buff) # Imprime a mensagem do buffer
	else: # senao
		print('error%d'%answer) # Imprime a mensagem de erro
		return False # retorna ao falso
	return True # retorna ao verdadeiro 

def power_on(power_key):
	print('SIM7600X is starting:') # Imprime a mensagem de starting do gsm
	# configuração das portas gpio
	GPIO.setmode(GPIO.BCM) 
	GPIO.setwarnings(False)
	GPIO.setup(power_key,GPIO.OUT)
	time.sleep(0.1) # espera 1 milissimo 
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(2) # espera 2 segundos
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(20) # espera 20 segundos
	ser.flushInput()
	print('SIM7600X is ready') # Imprime que esta tudo bem

def power_down(power_key):
	print('SIM7600X is loging off:') # Imprime quando acabar tudo
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(3) # espera 3 segundos
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(18) # espera 18 segundos
	print('Good bye') # Imprime um byee

# Função de callback para a interrupção do sensor
def callback_sensor(channel):
    global pulsos
    pulsos += 1

def read_voltage():
    voltage = (GPIO.input(CurrentSensorPin) * 3.3 / 1024) * VREF
    return voltage

def calculate_current(voltage):
    current = voltage / 120.0 # Sense Resistor:120ohm
    return current

# Configurar a interrupção no pino de saída do sensor
GPIO.add_event_detect(OUT_PIN, GPIO.FALLING, callback=callback_sensor)

# Leitura do sensor de umidade do solo com MCP3008
def read_mcp3008(channel):
    """Função para ler o valor de um canal específico do MCP3008"""
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Mapeamento dos valores lidos do MCP3008 para umidade do solo
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Loop principal do programa
channel = 0  # Canal do MCP3008 a ser lido (de 0 a 7)

try:
    power_on(power_key)
    while True:
        now = datetime.datetime.now()
        #ola
        voltage = read_voltage() * VREF / 1024.0
        current = voltage / 120.0
        depth = (4.00 - current) * (50 / 1 / 16.0)
        rounded = round(depth, 2)
        print("profundidade: {}cm".format(rounded))
        time.sleep(2)
        # Calcular o fluxo de água a cada segundo
        tempo_atual = time.time()
        delta_tempo = tempo_atual - tempo_anterior
        tempo_anterior = tempo_atual
        # Calcular o fluxo de água em L/min
        fluxo = pulsos / (delta_tempo * 60) * 7.5  # 7.5 é uma constante de calibração para o sensor YF-B5
        # reaniciar
        pulsos = 0
        # Leitura do sensor de umidade do solo
        channel = 0 
        value = read_mcp3008(channel)
        voltage = value * 3.3 / 1023  # Converter valor lido para tensão em Volts (3.3V é a tensão de referência do Raspberry Pi)
        soil_moisture = map_value(voltage, 0, 1.2, 0, 100)
        print(soil_moisture)
        rain_sensor_state = GPIO.input(RAIN_DROP_PIN)
        if now.hour == 17 and now.minute == 39:
            # Controle da bomba com base na umidade do solo e no fluxo de água
            if rain_sensor_state == 1: 
                print("Sem chuva - ligando a bomba")
                GPIO.output(VALVE_PIN, GPIO.HIGH)
                GPIO.output(RELAY_PIN, GPIO.HIGH)
                time.sleep(20)
                print("Fluxo de água: {:.2f} L/min".format(fluxo))
                time.sleep(2)
                GPIO.output(RELAY_PIN, GPIO.LOW)
                GPIO.output(VALVE_PIN, GPIO.LOW)
                SendShortMessage(phone_number, text_message1)
                time.sleep(10)
            elif rain_sensor_state == 0:
                print("Com chuva - Desligando a bomba")
                GPIO.output(RELAY_PIN, GPIO.LOW)
                SendShortMessage(phone_number, text_message1 )
                time.sleep(10)
                
except Exception as e: # Add the specific exception to catch, and print the error message
    print(f"An error occurred: {str(e)}")
    if ser is not None:
        ser.close()
    GPIO.cleanup()

#finally:
    # Limpar a configuração dos pinos GPIO
 #   GPIO.cleanup()

#soil_moisture > 140
#GPIO.output(PUMP_PIN, GPIO.LOW)
#sys.exit(0)
#soil_moisture > 163 and 
#soil_moisture < 160 or
