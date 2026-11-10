from pico2d import *
import game_world
import game_framework
from boy import Boy
from bird import Bird, FLIGHT_SPEED_PPS, FRAME_COUNT
from grass import Grass

boy = None
BIRD_START_POSITIONS = [
    (90, 430), (245, 500), (400, 355), (555, 455), (710, 530),
    (865, 390), (1020, 490), (1175, 345), (1330, 445), (1485, 525),
]


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    for index, (x, y) in enumerate(BIRD_START_POSITIONS):
        speed = FLIGHT_SPEED_PPS * (0.9 + (index % 5) * 0.05)
        bird = Bird(
            x, y,
            frame=index * FRAME_COUNT / len(BIRD_START_POSITIONS),
            speed=speed
        )
        game_world.add_oject(bird)

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()








