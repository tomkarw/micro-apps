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
    led1 = machine.Pin(config.LED1_PIN, machine.Pin.OUT)
    led2 = machine.Pin(config.LED2_PIN, machine.Pin.OUT)

    for _ in range(3):
        led1.off()
        led2.on()
        time.sleep(0.5)
        led1.on()
        led2.off()
        time.sleep(0.5)

    led1.on()
    led2.on()


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


def call_webhook():
    print('Invoking webhook')
    response = urequests.post(config.WEBHOOK_URL)
    if response is not None and response.status_code < 400:
        print('Webhook invoked')
    else:
        print('Webhook failed')
        raise RuntimeError('Webhook failed')


def run():
    try:
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            connect_wifi()
            call_webhook()
    except Exception as e:
        sys.print_exception(e)
        show_error()
    if not is_debug():
        machine.deepsleep()


run()
