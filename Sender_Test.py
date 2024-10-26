#This code will generate a PWM signal with a varying duty cycle (0-100%)
#It will send the duty cycle by means of serial communication (UART) to Pico2
#Lastly it will wait for a response from Pico2 with the measured ADC value

from machine import Pin, UART, PWM
import time

#Before coding we need to set up the GPIO pins for the PWM

PWM_Pin = PWM(Pin(0)) #assigns pin J1 as the PWM output
PWM_Pin.freq(1000) #sets the PWM frequency to 1kHz

#Next we need to setup the UART (referring to lab 2 manual)
#Baud rate needs to be the same on both Pico1 and Pico2

uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9)) #Reference to the Expansion Board Pin Config
uart.init(bits=8, parity=None, stop=1)

#Now we need to create a function to generate a variable duty cycle and print it

def set_pwm_duty_cycle (duty):
    PWM_Pin.duty_u16(int(duty*6535/100)) #this converts the duty cycle percentage into a 16-bit value
    print(f"Sending duty cycle of value: {duty}%") #informs user of duty-cylce value being transmitted
    uart.write(f"{duty}") #sends the duty cycle to Pico2 using UART serial communication as an f-string

#Now we need to use a loop (While) that will continue until there is no longer any signal being sent between the Picos

while True:
    desired_duty_cycle = 75 #For testing purposes we will assign a dutcy cyle of 75%
    set_pwm_duty_cycle(desired_duty_cycle) #Calls our function and generates the PWM signal with duty cycle of 75%

    if uart.any():
        measured_value = uart.read().decode("utf-8")
        print(f"Measured ADC value is: {measured_value}")
        time.sleep(1)

    time.sleep(5) #delay for stability before restarting cycle
