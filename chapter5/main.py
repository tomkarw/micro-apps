import dht
import time
import network
import config
import sys
import urequests
import machine


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
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config: ', sta_if.ifconfig())


def call_webhook(url, data):
    print('Invoking webhook')
    response = urequests.post(url, json=data)
    if response is not None and response.status_code < 400:
        print('Webhook invoked')
    else:
        print('Webhook failed')
        raise RuntimeError('Webhook failed')


def button_pressed():
    button = machine.Pin(config.BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    pressed_time = 0
    while not button.value():
        time.sleep(1)
        pressed_time += 1
    return pressed_time


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


def deepsleep():
    print('Going into deepsleep for {seconds} seconds...'.format(
        seconds=config.LOG_INTERVAL))
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0,wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, config.LOG_INTERVAL * 1000)
    machine.deepsleep()


def run():
    try:
        connect_wifi()
        temperature, humidity = get_temperature_and_humidity()
        log_weather_data(temperature, humidity)
    except Exception as e:
        sys.print_exception(e)
        show_error()
    if not is_debug():
        deepsleep()


run()
