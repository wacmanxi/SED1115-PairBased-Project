from machine import Pin, UART, PWM, ADC
import time

# Initialize PWM on Pin 0 and set frequency to 1kHz
pwm_pin = PWM(Pin(0))
pwm_pin.freq(1000)

# Initialize ADC on Pin 26 (Potentiometer input)
potentiometer = ADC(Pin(26))

# Initialize UART communication (same settings on both Picos)
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1)

def read_potentiometer():
    """Read the potentiometer value (0-65535) and convert to duty cycle (0-100%)."""
    raw_value = potentiometer.read_u16()
    duty_cycle = (raw_value / 65535) * 100  # Convert to percentage
    return round(duty_cycle, 2)

def set_pwm_duty_cycle(duty):
    """Set the PWM duty cycle and transmit it via UART."""
    pwm_pin.duty_u16(int(duty * 6535 / 100))  # Convert percentage to 16-bit value
    print(f"Sending duty cycle: {duty}%")
    uart.write(f"{duty}\n")  # Send duty cycle as a string with newline

def read_adc_value():
    """Simulate reading an ADC value and convert it to a percentage (for testing)."""
    raw_value = pwm_pin.duty_u16()  # Optional: Mock PWM reading, replace with real ADC if needed
    percentage = (raw_value / 65535) * 100
    return round(percentage, 2)

while True:
    # Read the potentiometer value and set the PWM duty cycle
    current_duty_cycle = read_potentiometer()
    set_pwm_duty_cycle(current_duty_cycle)

    # Check if data was received via UART
    if uart.any():
        received_value = uart.read().decode("utf-8").strip()
        print(f"Received duty cycle: {received_value}%")

    # Measure the ADC value for the PWM signal
    measured_adc = read_adc_value()
    print(f"Measured ADC value: {measured_adc}%")

    # Send the measured ADC value to the other Pico
    uart.write(f"{measured_adc}\n")

    time.sleep(1)  # Delay to avoid flooding the UART
