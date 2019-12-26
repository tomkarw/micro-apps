import machine
import time

LED1_PIN = 2  # D4
LED2_PIN = 16  # D0
BUTTON_PIN = 14  # D5


def blink():
    led1 = machine.Pin(LED1_PIN, machine.Pin.OUT)
    led2 = machine.Pin(LED2_PIN, machine.Pin.OUT)
    button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

    while button.value():
        led1.off()
        led2.on()
        time.sleep(0.5)
        led1.on()
        led2.off()
        time.sleep(0.5)

    led1.on()
    led2.on()


blink()
