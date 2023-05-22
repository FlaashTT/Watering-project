import RPi.GPIO as GPIO  # Importa a biblioteca RPi.GPIO para controlar os pinos GPIO do Raspberry Pi
import serial  # Importa a biblioteca serial para comunicar com o módulo SIM7600X
import time  # Importa a biblioteca time para adicionar pausas no código
import datetime

ser = serial.Serial("/dev/ttyS0",115200)  # Define a porta serial utilizada para se comunicar com o módulo SIM7600X e a taxa de transmissão
ser.flushInput()  # Limpa o buffer de entrada da porta serial
now = datetime.datetime.now()

phone_number = '+351'  # Número de telefone para onde serão enviadas as mensagens
text_message1 = 'Sem chuva!'  # Mensagem a ser enviada caso não haja chuva
text_message = 'Com chuva!'  # Mensagem a ser enviada caso haja chuva
power_key = 6  # Define o pino GPIO que será utilizado para ligar/desligar o módulo SIM7600X
rec_buff = ''  # Buffer para armazenar as respostas do módulo SIM7600X

# Configuração do pino do sensor de chuva
RAIN_SENSOR_PIN = 16
GPIO.setmode(GPIO.BCM)  # Configura o modo de numeração dos pinos como BCM
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)  # Define o pino do sensor de chuva como entrada

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

try:
    power_on(power_key)
    while True:
        now = datetime.datetime.now() # adiciona um hora
        if now.hour == 16 and now.minute == 57:
            if GPIO.input(RAIN_SENSOR_PIN) == GPIO.HIGH: # se o rain tiver high
                print("Sem chuva") # print "Sem chuva"
                SendShortMessage(phone_number, text_message1) # envia a messagem para o tal numero
                time.sleep(10) # espera 25 segundos
            else: # otherwise
                print("Chuva detectada") # print "Chuva detectada"
                SendShortMessage(phone_number, text_message) # envia a messagem para o tal numero
                time.sleep(10) # espera 25 segundos
except Exception as e: # Adciona caso houver algo erro na consola
    print(f"An error occurred: {str(e)}")
    if ser is not None:
        ser.close()
    GPIO.cleanup()

