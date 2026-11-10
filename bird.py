"""Frame-based flight animation and motion for the bird flock.

The sheet has 14 frames arranged in five columns at 12 frames per second, so
one wingbeat loop lasts about 1.17 seconds. The 183x168 source cells render at
0.4 scale (about 73x67 pixels) for visibility on the 1600x600 game canvas.
Using the game's 10 pixels per 0.3 meters, a 5 m/s cruising speed is about
167 pixels per second; the flock varies that speed by +/-10 percent.
"""

from math import pi, sin

import game_framework
from pico2d import get_canvas_width, load_image


SPRITE_SHEET_WIDTH = 918
SPRITE_SHEET_HEIGHT = 506
FRAME_WIDTH = 183
FRAME_HEIGHT = 168
FRAME_COLUMNS = 5
FRAME_COUNT = 14
FRAMES_PER_SECOND = 12.0
SPRITE_SCALE = 0.4
PIXELS_PER_METER = 10.0 / 0.3
FLIGHT_SPEED_MPS = 5.0
FLIGHT_SPEED_PPS = FLIGHT_SPEED_MPS * PIXELS_PER_METER
FLIGHT_BOB_AMPLITUDE = 3.0


class Bird:
    image = None

    def __init__(self, x, y, direction=1, frame=0, speed=FLIGHT_SPEED_PPS):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x = x
        self.y = y
        self.direction = 1 if direction >= 0 else -1
        self.speed = speed
        self.frame = frame % FRAME_COUNT

    def update(self):
        self.frame = (
            self.frame + FRAMES_PER_SECOND * game_framework.frame_time
        ) % FRAME_COUNT
        self.x += self.direction * self.speed * game_framework.frame_time

        half_width = FRAME_WIDTH * SPRITE_SCALE / 2
        left_edge = half_width
        right_edge = get_canvas_width() - half_width
        while self.x < left_edge or self.x > right_edge:
            if self.x < left_edge:
                self.x = left_edge + (left_edge - self.x)
                self.direction = 1
            elif self.x > right_edge:
                self.x = right_edge - (self.x - right_edge)
                self.direction = -1

    def draw(self):
        frame_index = int(self.frame)
        column = frame_index % FRAME_COLUMNS
        row_from_top = frame_index // FRAME_COLUMNS
        source_x = int(column * SPRITE_SHEET_WIDTH / FRAME_COLUMNS)
        source_y = int(
            (2 - row_from_top) * SPRITE_SHEET_HEIGHT / 3
        )
        draw_y = self.y + FLIGHT_BOB_AMPLITUDE * sin(
            2 * pi * self.frame / FRAME_COUNT
        )

        Bird.image.clip_composite_draw(
            source_x, source_y, FRAME_WIDTH, FRAME_HEIGHT,
            0, 'h' if self.direction < 0 else '',
            self.x, draw_y,
            FRAME_WIDTH * SPRITE_SCALE, FRAME_HEIGHT * SPRITE_SCALE
        )
