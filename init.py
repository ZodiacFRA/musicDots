import random

import utils
import config
import display_utils
from Ball import Ball
from Wall import Wall
from Vector2 import Vector2


def balls(balls_nbr, walls, px_window_size, sample_nbr, shuffle=False):
    # Create the available notes, based on the scale and the number of balls
    offset = 24
    scale = [n + offset for n in config.scale]
    notes = scale
    while len(notes) < balls_nbr:
        notes += [n + 12 for n in scale]
    notes = [n % sample_nbr for n in notes]
    color_list = display_utils.get_color_list(balls_nbr)
    balls = []
    # base_velocity = random.randint(-500, 500)
    radius = 32
    speeds_list = [2 * exp for exp in range(20, 100)]
    tile_nbr = px_window_size // radius
    for idx in range(balls_nbr):
        retry_count = 0
        new_ball = None
        while retry_count < 20:
            base_velocity = random.choice(speeds_list)
            velocity = Vector2(
                random.choice([-1, 1]) * base_velocity,
                random.choice([-1, 1]) * base_velocity,
            )
            pos = (
                Vector2(
                    random.randint(1, tile_nbr.x - 2),
                    random.randint(1, tile_nbr.y - 2),
                )
                * radius
            )
            new_ball = Ball(
                pos=pos,
                velocity=velocity,
                radius=radius,
                bounciness=1,
                color=color_list[idx],
            )
            if utils.is_valid_pos(new_ball, walls, balls):
                new_ball.sound_idx = notes[idx]
                # new_ball.sound_idx = notes.pop(random.choice(range(len(notes))))
                balls.append(new_ball)
                break
    if shuffle:
        random.shuffle(balls)
    return balls


def walls(px_window_size):
    res = [
        Wall(Vector2(px_window_size.x, 0), Vector2(0, 0)),
        Wall(
            Vector2(px_window_size.x, px_window_size.y),
            Vector2(px_window_size.x, 0),
        ),
        Wall(
            Vector2(0, px_window_size.y),
            Vector2(px_window_size.x, px_window_size.y),
        ),
        Wall(Vector2(0, 0), Vector2(0, px_window_size.y)),
    ]
    # res += utils.add_cross(px_window_size)
    return res


def dots(px_window_size):
    pass
