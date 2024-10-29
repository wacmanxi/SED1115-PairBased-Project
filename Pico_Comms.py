# This code enables two Raspberry Pi Picos to read and write PWM signals based on ADC values
# Both Picos can control the duty cycle using a potentiometer connected to Pin 26
# UART serial communication allows each Pico to send the duty cycle and receive the measured ADC value from the other
# Lastly, each Pico adjusts its PWM output according to the potentiometer reading and displays all values
# This code uses MIT software license and ChatGPT to help with readability and debugging

from machine import Pin, UART, PWM, ADC  # Modules for PWM, UART, and ADC functionality
import time  # Time module used for delays

# Before coding, we need to set up the GPIO pins for the PWM

PWM_Pin = PWM(Pin(0))  # Assigns Pin 0 (J1) as the PWM output
PWM_Pin.freq(1000)  # Sets the PWM frequency to 1 kHz based on standard

# Next we need to set up ADC on Pin 26 to read the potentiometer values (for mapping to the duty cycle)

potentiometer = ADC(Pin(26))  # Potentiometer input on Pin 26 (reads values from 0-65535)

# Next we need to set up the UART communication (referencing Lab 2 manual)
# Baud rate needs to be the same on both Pico1 and Pico2 to ensure proper communication

uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))  # TX on Pin 8, RX on Pin 9
uart.init(bits=8, parity=None, stop=1)  # Initializes UART settings: 8-bit data, no parity, 1 stop bit

# Now we need to create a function to read the potentiometer value and convert it to a duty cycle (0-100%)

def read_potentiometer():
    raw_value = potentiometer.read_u16()  # Reads the raw ADC value (range: 0-65535)
    duty_cycle = (raw_value / 65535) * 100  # Converts the raw value to a percentage (0-100%)
    return round(duty_cycle, 2)  # Rounds the duty cycle value to 2 decimal places for better readability

# Next we create a function to set the PWM duty cycle and transmit it using UART serial communication to the other Pico

def set_pwm_duty_cycle(duty):
    PWM_Pin.duty_u16(int(duty * 6535 / 100))  # Converts the duty cycle percentage to a 16-bit value
    print(f"Sending duty cycle of value: {duty}%")  # Informs the user of duty cycle value being transmitted
    uart.write(f"{duty}\n")  # Sends the duty cycle via UART as an f- string

# Now we need a function that simulates the measurement of the ADC value

def read_adc_value():
    adc_value = PWM_Pin.duty_u16()  # Reads the duty cycle as a simulated ADC value
    adc_percentage = (adc_value / 6535) * 100  # Converts the 16-bit value to a percentage (0-100%)
    return round(adc_percentage, 2)  # Rounds to 2 decimal places for readability

# Lastly, we need to create an infinite loop to continuously adjust the PWM signal and communicate with the other Pico

while True:
    # Reads the potentiometer value and sets the PWM duty cycle accordingly
    desired_duty_cycle = read_potentiometer()  # Receives the current duty cycle from the potentiometer
    set_pwm_duty_cycle(desired_duty_cycle)  # Sets the PWM output using the desired duty cycle

    # Checks if there is incoming data from the other Pico via UART serial communication
    if uart.any():  # If data is available on UART
        received_value = uart.read().decode("utf-8").strip()  # Reads and decodes the received data using strip which handles the whitespace
        print(f"Received duty cycle: {received_value}%")  # Displays the received duty cycle

    # Measures the ADC value
    measured_adc = read_adc_value()  # Gets the current ADC value (in percentage)
    print(f"Measured ADC value: {measured_adc}%")  # Prints the measured ADC value

    # Sends the measured ADC value to the other Pico via UART serial communication
    uart.write(f"{measured_adc}\n")  # Transmits the ADC value as an f-string with a new line

    # Adds a short delay to prevent flooding the UART and ensure stable communication
    time.sleep(2)  # 2-second delay implemented for stability before the next iteration

