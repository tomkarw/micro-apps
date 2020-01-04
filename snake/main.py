import time

import machine
import ssd1306

from snake import Snake

# LED1_PIN = 2  # D4
# LED2_PIN = 16  # D0

BUTTON_LEFT_PIN = 5  # D1
BUTTON_RIGHT_PIN = 4  # D2

DISPLAY_SCL_PIN = 0  # D3
DISPLAY_SDA_PIN = 14  # D5

# led1 = machine.Pin(LED1_PIN, machine.Pin.OUT)
# led2 = machine.Pin(LED2_PIN, machine.Pin.OUT)

button_left = machine.Pin(BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button_right = machine.Pin(BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

i2c = machine.I2C(scl=machine.Pin(DISPLAY_SCL_PIN),
                  sda=machine.Pin(DISPLAY_SDA_PIN))
if 60 not in i2c.scan():
    raise RuntimeError('Cannot find display')
display = ssd1306.SSD1306_I2C(128, 64, i2c)


class SnakeGame:

    def __init__(self, width, height, fps, rate, display, pixel):
        self.width = width
        self.height = height
        self.pixel = pixel
        self.display = display

        self.fps = fps
        self.rate = rate

        self.snake = Snake(width//pixel, height//pixel)

    # TODO: optimise drawing (don't have to redraw everything)
    def draw(self):
        self.display.fill(0)
        for segment in self.snake.body:
            self.display.fill_rect(
                segment[0]*self.pixel,
                segment[1]*self.pixel, 4, 4, 1
            )
        self.display.fill_rect(
            self.snake.food[0]*self.pixel,
            self.snake.food[1]*self.pixel, 4, 4, 1
        )
        self.display.show()

    # TODO: Best scores ranking with name input
    def game_over(self):
        time.sleep(1.5)
        self.display.fill(0)
        self.display.text('Game Over!', 0, 0)
        self.display.text('Score: {s}'.format(s=len(self.snake.body)), 0, 16)
        self.display.text('Click any button', 0, 32)
        self.display.text('to play again.', 0, 48)
        self.display.show()

    def run(self):
        i = 0
        right_state = 0
        left_state = 0
        while True:
            right = not button_right.value()
            left = not button_left.value()
            if right and not right_state:
                self.snake.turn_right()
            if left and not left_state:
                self.snake.turn_left()
            right_state = right
            left_state = left

            if i == 0:
                if self.snake.has_collided():
                    self.game_over()
                    break
                self.snake.move(ate=self.snake.ate())
                self.draw()

            i = (i+1) % self.rate
            time.sleep(1/self.fps)


def main():
    while True:
        game = SnakeGame(
            width=128,
            height=64,
            fps=960,
            rate=16,
            display=display,
            pixel=4
        )
        game.run()
        while button_left.value() and button_right.value():
            time.sleep(0.1)


main()
