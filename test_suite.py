import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Constants for GPIO pins
led_pin = 11

# Constants for ADC configuration
spi_port = 0
spi_device = 0

# Threshold values for light and sound sensors
light_threshold = 500  # Adjust as needed
sound_threshold = 500  # Adjust as needed

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)

# Initialize ADC
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spi_port, spi_device))

def blink_led(times, interval):
    for _ in range(times):
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(interval)

def read_light_sensor(duration, interval):
    start_time = time.time()
    while (time.time() - start_time) < duration:
        light_value = mcp.read_adc(0)
        brightness = "bright" if light_value > light_threshold else "dark"
        print(f"Light sensor value: {light_value}, {brightness}")
        time.sleep(interval)

def read_sound_sensor(duration, interval):
    start_time = time.time()
    while (time.time() - start_time) < duration:
        sound_value = mcp.read_adc(1)
        print(f"Sound sensor value: {sound_value}")
        if sound_value > sound_threshold:
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(led_pin, GPIO.LOW)
        time.sleep(interval)

try:
    while True:
        # Blink LED 4 times with intervals of 500ms
        blink_led(4, 0.25)

        # Read light sensor for about 5 seconds
        read_light_sensor(5, 0.1)

        # Blink LED 10 times with intervals of 200ms
        blink_led(10, 0.1)

        # Read sound sensor for about 5 seconds
        read_sound_sensor(5, 0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
