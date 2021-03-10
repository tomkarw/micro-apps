import time

try:
    from .config import *
except ValueError:
    from config import *
try:
    from .snake import Snake
except ValueError:
    from snake import Snake
try:
    from .scoreboard import ScoreBoard
except ValueError:
    from scoreboard import ScoreBoard


class SnakeGame:

    def __init__(self, width, height, fps, rate, display, pixel):
        self.width = width
        self.height = height
        self.pixel = pixel
        self.display = display

        self.fps = fps
        self.rate = rate

        self.snake = Snake(width // pixel, height // pixel)

        self.score_file = 'scores.txt'

    # TODO: optimise drawing (don't have to redraw everything)
    def draw(self):
        self.display.fill(0)
        for segment in self.snake.body:
            self.display.fill_rect(
                segment[0] * self.pixel,
                segment[1] * self.pixel, 4, 4, 1
            )
        self.display.fill_rect(
            self.snake.food[0] * self.pixel,
            self.snake.food[1] * self.pixel, 4, 4, 1
        )
        self.display.show()

    def game_over(self):
        score = len(self.snake.body)
        self.display.fill(0)
        self.display.text('Game Over!', 0, 0)
        self.display.text('Score: {s}'.format(s=score), 0, 16)
        self.display.show()
        time.sleep(1.5)
        sb = ScoreBoard(self.score_file, self.display)
        name = sb.get_name()
        sb.save_score_to_file(name, score)
        sb.show_scoreboard()

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
                    time.sleep(1.5)
                    self.game_over()
                    break
                self.snake.move(ate=self.snake.ate())
                self.draw()

            i = (i + 1) % self.rate
            time.sleep(1 / self.fps)


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
