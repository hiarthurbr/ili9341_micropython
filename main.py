# https://wokwi.com/projects/410188788552836097
print("Hello, ESP32!")

from machine import Pin, SPI

red = Pin(25, Pin.OUT)
green = Pin(26, Pin.OUT)
blue = Pin(27, Pin.OUT)
red.value(0)
green.value(0)
blue.value(1)

import dht
from ili9341 import Display, color565
from time import sleep
import time


messages = {
    "on_init": "Bem vindo",
    "on_exit": "Ate a proxima"
}

# Create a DHT22 object
dht_sensor = dht.DHT22(Pin(13))

display = Display(
    SPI(2, baudrate=32000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19)),
    dc=Pin(2), cs=Pin(15), rst=Pin(4),
    w=320, h=240, r=0
)

button = Pin(12, Pin.IN, Pin.PULL_DOWN)


def erase():
    display.set_pos(0,0)
    display.erase()

def led_on():
    red.value(1)
    green.value(0)
    blue.value(1)

def led_off():
    red.value(0)
    green.value(1)
    blue.value(1)

def led_trans():
    red.value(0)
    green.value(0)
    blue.value(1)

def print_value():
    try:
        # Trigger the sensor to take a measurement
        dht_sensor.measure()

        # Read the temperature and humidity
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # Print the results
        display.print('{}\n{}'.format(
            'Temperature: {}C'.format(temperature),
            'Humidity: {}%'.format(humidity)
            )
        )

    except OSError as e:
        print('Failed to read from DHT22 sensor:', e)

state = {
    "on": False,
    "trans": False,
}

if (state["on"]):
    led_on()
else:
    led_off()

print("Started main loop")
while True:
    erase()
    if (button.value() and not state["trans"]):
        print("Detected button press, changing state")
        state["trans"] = True
        led_trans()

    if (state["on"]):
        if (state["trans"]):
            display.print(messages["on_exit"])
        else:
            print_value()
    else:
        if (state["trans"]):
            display.print(messages["on_init"])

    if (state["trans"]):
        state["on"] = bool(state["on"] ^ state["trans"])
        state["trans"] = False
        if (state["on"]):
            led_on()
        else:
            led_off()
        print("New state {}".format(state))
    sleep(0.1)
