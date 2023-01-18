import random

import cmasher as cmr

from physics import *
from Vector2 import Vector2


def init_balls(balls_nbr, walls, px_window_size, sample_nbr):
    # Create the available notes, based on the scale and the number of balls
    offset = 12
    scale = [n + offset for n in config.scale]
    notes = scale
    while len(notes) < balls_nbr:
        notes += [n + 12 for n in scale]
    notes = [n % sample_nbr for n in scale]
    # https://matplotlib.org/stable/tutorials/colors/colormaps.html
    # cool
    color_list = cmr.take_cmap_colors("viridis", balls_nbr, return_fmt="int")

    balls = []
    # base_velocity = random.randint(-500, 500)
    radius = 8
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
            if is_valid_pos(new_ball, walls, balls):
                new_ball.sound_idx = notes[idx]
                # new_ball.sound_idx = notes.pop(random.choice(range(len(notes))))
                balls.append(new_ball)
                break
    return balls


def is_valid_pos(new_ball, walls, balls):
    for wall in walls:
        if process_wall_collision(wall, new_ball, detection_only=True):
            return False
    for ball in balls:
        if process_ball_collision(new_ball, ball, use_mass=False, detection_only=True):
            return False
    return True
