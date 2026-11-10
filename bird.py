import game_framework
from pico2d import load_image


SPRITE_SHEET_WIDTH = 918
SPRITE_SHEET_HEIGHT = 506
FRAME_WIDTH = 183
FRAME_HEIGHT = 168
FRAME_COLUMNS = 5
FRAME_COUNT = 14
FRAMES_PER_SECOND = 12.0
SPRITE_SCALE = 0.4


class Bird:
    image = None

    def __init__(self, x, y, frame=0):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x = x
        self.y = y
        self.frame = frame % FRAME_COUNT

    def update(self):
        self.frame = (
            self.frame + FRAMES_PER_SECOND * game_framework.frame_time
        ) % FRAME_COUNT

    def draw(self):
        frame_index = int(self.frame)
        column = frame_index % FRAME_COLUMNS
        row_from_top = frame_index // FRAME_COLUMNS
        source_x = int(column * SPRITE_SHEET_WIDTH / FRAME_COLUMNS)
        source_y = int(
            (2 - row_from_top) * SPRITE_SHEET_HEIGHT / 3
        )

        Bird.image.clip_composite_draw(
            source_x, source_y, FRAME_WIDTH, FRAME_HEIGHT,
            0, '', self.x, self.y,
            FRAME_WIDTH * SPRITE_SCALE, FRAME_HEIGHT * SPRITE_SCALE
        )
