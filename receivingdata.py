import time
from machine import Pin, UART


uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1)

while True:
    
    uart.write(b"wagwaan")
    time.sleep(1)

    if uart.any():
        message = uart.read().decode('utf-8')
        print(message)
    
    time.sleep(1)
