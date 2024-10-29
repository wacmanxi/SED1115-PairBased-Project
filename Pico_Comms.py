#This code will generate a PWM signal with a varying duty cycle (0-100%)
#It will send the duty cycle by means of serial communication (UART) to Pico2
#Lastly it will wait for a response from Pico2 with the measured ADC value
#This code made use of Licenses from MIT

from machine import Pin, UART, PWM, ADC
import time
import random

#Before coding we need to set up the GPIO pins for the PWM

PWM_Pin = PWM(Pin(0)) #assigns pin J1 as the PWM output
PWM_Pin.freq(1000) #sets the PWM frequency to 1kHz

#Define adc pins

adc = ADC(Pin(26))

#Next we need to setup the UART (referring to lab 2 manual)
#Baud rate needs to be the same on both Pico1 and Pico2

uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9)) #Reference to the Expansion Board Pin Config
uart.init(bits=8, parity=None, stop=1)

#Now we need to create a function to generate a variable duty cycle and print it

def set_pwm_duty_cycle (duty):
    PWM_Pin.duty_u16(int(duty*6535/100)) #this converts the duty cycle percentage into a 16-bit value
    print(f"Sending duty cycle of value: {duty}%") #informs user of duty-cylce value being transmitted
    uart.write(f"{duty}") #sends the duty cycle to Pico2 using UART serial communication as an f-string

def read_adc_value():
    """Reads the ADC value and converts it to a percentage (0-100%)."""
    raw_value = adc.read_u16()  
    percentage = (raw_value / 65535) * 100  # Convert to percentage
    return round(percentage, 2)  # Return rounded value 

#Now we need to use a loop (While) that will continue until there is no longer any signal being sent between the Picos

while True:
    desired_duty_cycle = random.randint(0,100) #Generates a random duty cycle between 0%-100%
    set_pwm_duty_cycle(desired_duty_cycle) #Calls our function and generates the PWM signal with duty cycle of 75%
    
    if uart.any():
        measured_value = uart.read().decode("utf-8")
        print(f"Measured ADC value is: {measured_value}")
        time.sleep(1)

    # Check if a duty cycle value was received from Pico 1
    if uart.any():
        duty_cycle = uart.read().decode("utf-8").strip()  # Read and decode the duty cycle value
        print(f"Received Duty Cycle: {duty_cycle}%")

        # Measure the ADC value corresponding to the PWM signal
        measured_value = read_adc_value()
        print(f"Measured ADC Value: {measured_value}%")

        # Send the measured ADC value back to Pico 1 
        uart.write(f"{measured_value}")

    time.sleep(5) #delay for stability before restarting cycle
