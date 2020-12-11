# Standard library
import time
import sys

# MicroPython specific modules
import machine
import network
import urequests
import framebuf

# Components
import ssd1306
import dht

# Custom files
import config
import writer
import freesans20


def is_debug():
    debug = machine.Pin(config.DEBUG_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    if debug.value() == 0:
        print('Debug mode detected.')
        return True
    return False


def show_error():
    led = machine.Pin(config.LED_PIN, machine.Pin.OUT)

    for _ in range(3):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

    led.on()


def connect_wifi():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to Wifi...')
        sta_if.active(True)
        sta_if.connect(*config.WIFI_GIERYMSKIEGO)
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config: ', sta_if.ifconfig())


def get_temperature_and_humidity():
    d = dht.DHT22(machine.Pin(config.DHT22_PIN))
    d.measure()
    return d.temperature(), d.humidity()


def log_weather_data(temperature, humidity):
    print('Invoking weather webhook')
    url = config.WEBHOOK_WEATHER_URL.format(temperature=temperature,
                                            humidity=humidity)
    response = urequests.get(url)
    if response is not None and response.status_code < 400:
        print('Webhook invoked')
    else:
        print('Webhook failed')
        raise RuntimeError('Webhook failed')


def deepsleep(sleep_time):
    print('Going into deepsleep for {seconds} seconds...'.format(
        seconds=sleep_time))
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, sleep_time * 1000)
    machine.deepsleep()


def load_image(filename):
    with open(filename, 'rb') as f:
        f.readline()
        f.readline()
        width, height = [int(v) for v in f.readline().split()]
        data = bytearray(f.read())
    return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)


def display_temperature_and_humidity(temperature, humidity):
    i2c = machine.I2C(scl=machine.Pin(config.DISPLAY_SCL_PIN),
                      sda=machine.Pin(config.DISPLAY_SDA_PIN))
    if 60 not in i2c.scan():
        raise RuntimeError('Cannot find display')

    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    font_writer = writer.Writer(display, freesans20)

    temperature_pbm = load_image('temperature.pbm')
    units_pbm = load_image('celsius.pbm')
    humidity_pbm = load_image('humidity.pbm')
    percent_pbm = load_image('percent.pbm')

    display.fill(0)
    display.rect(0, 0, 128, 64, 1)
    display.line(64, 0, 64, 64, 1)
    display.blit(temperature_pbm, 24, 4)
    display.blit(humidity_pbm, 88, 4)
    display.blit(units_pbm, 28, 52)
    display.blit(percent_pbm, 92, 52)

    text = '{:.1f}'.format(temperature)
    textlen = font_writer.stringlen(text)
    font_writer.set_textpos((64 - textlen) // 2, 26)
    font_writer.printstring(text)

    text = '{:.1f}'.format(humidity)
    textlen = font_writer.stringlen(text)
    font_writer.set_textpos(64 + (64 - textlen) // 2, 26)
    font_writer.printstring(text)

    display.show()


def end_display():
    i2c = machine.I2C(scl=machine.Pin(config.DISPLAY_SCL_PIN),
                      sda=machine.Pin(config.DISPLAY_SDA_PIN))
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.poweroff()


def run():
    sleep_time = config.LOG_INTERVAL
    try:
        start_time = time.time()
        # button = machine.Pin(config.BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
        # button_pressed = not button.value()
        connect_wifi()
        temperature, humidity = get_temperature_and_humidity()
        # TODO: log_weather... throws some heavy error if run after display...
        # if button_pressed:
        #     display_temperature_and_humidity(temperature, humidity)
        #     display_start_time = time.time()
        log_weather_data(temperature, humidity)
        # if button_pressed:
        #     time.sleep(config.DISPLAY_TIME - time.time() + display_start_time)
        #     end_display()
        sleep_time -= time.time() - start_time  # subtract time spent on processing
    except Exception as e:
        sys.print_exception(e)
        show_error()
    if not is_debug():
        deepsleep(sleep_time)


run()
