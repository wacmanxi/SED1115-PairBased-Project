from machine import Pin, UART, ADC
import time


uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9)) 
uart.init(bits=8, parity=None, stop=1)


adc = ADC(Pin(26))

def read_adc_value():
    """Reads the ADC value and converts it to a percentage (0-100%)."""
    raw_value = adc.read_u16()  
    percentage = (raw_value / 65535) * 100  # Convert to percentage
    return round(percentage, 2)  # Return rounded value 

while True:
    # Check if a duty cycle value was received from Pico 1
    if uart.any():
        duty_cycle = uart.read().decode("utf-8").strip()  # Read and decode the duty cycle value
        print(f"Received Duty Cycle: {duty_cycle}%")

        # Measure the ADC value corresponding to the PWM signal
        measured_value = read_adc_value()
        print(f"Measured ADC Value: {measured_value}%")

        # Send the measured ADC value back to Pico 1 
        uart.write(f"{measured_value}")

    time.sleep(1)  