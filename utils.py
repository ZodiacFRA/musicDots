import os

from physics import *
from Vector2 import Vector2
from Wall import Wall


def create_walls_from_points(points):
    res = []
    for idx, point in enumerate(points):
        res.append(Wall(points[idx], points[(idx + 1) % len(points)]))
    return res


def is_valid_pos(new_ball, walls, balls):
    for wall in walls:
        if process_wall_collision(wall, new_ball, detection_only=True):
            return False
    for ball in balls:
        if process_ball_collision(new_ball, ball, use_mass=False, detection_only=True):
            return False
    return True


def add_cross(px_window_size):
    divides = 3
    px_border_size = 64
    px_top_left = Vector2(px_border_size, px_border_size)
    px_bottom_right = px_window_size - px_top_left
    xm = [
        px_top_left.x,
        px_bottom_right.x // divides,
        px_bottom_right.x - px_bottom_right.x // divides,
        px_bottom_right.x,
    ]
    ym = [
        px_top_left.y,
        px_bottom_right.y // divides,
        px_bottom_right.y - px_bottom_right.y // divides,
        px_bottom_right.y,
    ]
    # Starting top left of the cross
    points = [
        # Top part + Right side
        Vector2(xm[0], ym[1]),
        Vector2(xm[1], ym[1]),
        Vector2(xm[1], ym[0]),
        Vector2(xm[2], ym[0]),
        Vector2(xm[2], ym[1]),
        Vector2(xm[3], ym[1]),
        Vector2(xm[3], ym[2]),
        # Bottom part + Left side
        Vector2(xm[2], ym[2]),
        Vector2(xm[2], ym[3]),
        Vector2(xm[1], ym[3]),
        Vector2(xm[1], ym[2]),
        Vector2(xm[0], ym[2]),
        # Last one is not needed as we'll auto close
    ]
    return create_walls_from_points(points)


def get_filepaths_from_dir(dirpath, extension=".wav"):
    return [
        os.path.join(dirpath, f) for f in os.listdir(dirpath) if f.endswith(extension)
    ]
