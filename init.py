import random

import utils
import config
import audio_utils
from Ball import Ball
from Vector2 import Vector2


def balls(walls, px_window_size, color_list, balls_nbr, shuffle=False):
    balls = []
    for idx in range(balls_nbr):
        balls.append(add_new_ball(idx, walls, px_window_size, color_list, balls))
    if shuffle:
        random.shuffle(balls)
    return balls


def add_new_ball(idx, walls, px_window_size, color_list, balls):
    speeds_list = [1, 2, 4]
    speeds_list = [2]
    retry_count = 0
    new_ball = None
    tile_nbr = px_window_size // config.balls_radius
    while retry_count < 10:
        retry_count += 1
        base_velocity = random.choice(speeds_list)
        velocity = Vector2(
            random.choice([-1, -1, 0, 1, 1]) * base_velocity,
            random.choice([-1, -1, 0, 1, 1]) * base_velocity,
        )
        pos = (
            Vector2(
                random.randint(1, tile_nbr.x - 2),
                random.randint(1, tile_nbr.y - 2),
            )
            * config.balls_radius
        )
        new_ball = Ball(
            id=idx,
            pos=pos,
            velocity=velocity,
            radius=config.balls_radius,
            bounciness=1,
            color=color_list[idx % len(color_list)],
        )
        if utils.is_valid_pos(new_ball, walls, balls):
            # new_ball.sound_idx = notes.pop(random.choice(range(len(notes))))
            # new_ball.sound_idx = notes.pop(random.choice(range(sample_nbr)))
            return new_ball


def walls(px_window_size):
    res = []
    # res += utils.add_cross(px_window_size)
    return res


def dots(color_list):
    res = []
    idx = 0
    for y in range(1, config.t_size.y):
        for x in range(1, config.t_size.x):
            new_ball = Ball(
                id=config.balls_nbr + idx,
                pos=Vector2(x=x, y=y) * config.balls_radius,
                velocity=Vector2(0, 0),
                radius=6,
                bounciness=1,
                color="#ffffff",
                # color=color_list[0],
            )
            res.append(new_ball)
            idx += 1
    return res
