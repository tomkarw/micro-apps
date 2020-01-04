import machine
import ssd1306

BUTTON_LEFT_PIN = 5  # D1
BUTTON_RIGHT_PIN = 4  # D2

DISPLAY_SCL_PIN = 0  # D3
DISPLAY_SDA_PIN = 14  # D5

button_left = machine.Pin(BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button_right = machine.Pin(BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

i2c = machine.I2C(
    scl=machine.Pin(DISPLAY_SCL_PIN),
    sda=machine.Pin(DISPLAY_SDA_PIN)
)
if 60 not in i2c.scan():
    raise RuntimeError('Cannot find display')
display = ssd1306.SSD1306_I2C(128, 64, i2c)
