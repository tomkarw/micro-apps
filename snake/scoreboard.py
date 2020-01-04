import time

try:
    from .config import *
except ValueError:
    from config import *

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class ScoreBoard:

    def __init__(self, scorefile, display):
        self.scorefile = scorefile
        self.display = display

    def get_name(self):
        d = self.display
        name = ''
        i = 0
        while len(name) < 3:
            d.fill(0)
            d.text('Red - change', 0, 0)
            d.text('Blue - accept', 0, 12)
            d.text('Name(3): {n}'.format(n=name), 0, 24)
            d.text('ABCDEFGHIJKLM', 0, 36)
            d.text('NOPQRSTUVWXYZ', 0, 48)
            shift = (i > 12)
            d.fill_rect(i*8-shift*8*13, 36+12*shift, 8, 8, 1)
            d.text(ALPHABET[i], i*8-shift*8*13, 36+12*shift, 0)
            d.show()
            right = not button_right.value()
            left = not button_left.value()
            if right:
                name += ALPHABET[i]
                i = 0
            if left:
                i = (i+1) % len(ALPHABET)
            time.sleep(0.05)
        return name

    # TODO: place text in the middle
    def show_scoreboard(self):
        d = self.display
        d.fill(0)
        d.show()
        d.text('Scoreboard:', 0, 0)
        with open(self.scorefile, 'r') as f:
            for i in range(1, 6):
                name, score = f.readline().strip('\n').split(',')
                d.text("{i}. {name} {score}".format(i=i, name=name, score=score),
                       0, i*10)
            d.show()
        while button_left.value() and button_right.value():
            time.sleep(0.1)

    def save_score_to_file(self, name, score):
        with open(self.scorefile, 'r') as f:
            scores = list(map(lambda x: x.split(','), f.read().split('\n')))[:20]
            scores += [[name, str(score)]]
            scores = sorted(scores, reverse=True, key=lambda x: int(x[1]))
        with open(self.scorefile, 'w') as f:
            f.write('\n'.join(list(map(','.join, scores))))
