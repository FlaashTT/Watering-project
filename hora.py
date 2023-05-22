import datetime

# Obtém a hora atual
now = datetime.datetime.now()

# Verifica se é hora de enviar a mensagem
if now.hour == 12 and now.minute == 43:
    # Envia a mensagem
    SendShortMessage(phone_number, text_message)
