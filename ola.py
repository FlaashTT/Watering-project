from machine import UART, Pin

TERMINATION_CHAR = '\x1a'

TXD_PIN = 'GP14'
RXD_PIN = 'GP15'
RST_PIN = 'GP22'

RST = Pin(RST_PIN, mode=Pin.OUT)
RST.value(0)
uart = UART(1, baudrate=9600, pins=(TXD_PIN, RXD_PIN))
RST.value(1)
