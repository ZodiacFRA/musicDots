import pygame
import cmasher as cmr

import config
from Vector2 import Vector2


def create_surface(px_window_size, alpha_value):
    s = pygame.Surface(px_window_size.to_int_tuple(), pygame.SRCALPHA)
    s.set_alpha(alpha_value)
    pygame.draw.rect(
        s,
        (0, 0, 0),
        pygame.Rect(0, 0, *px_window_size.to_int_tuple()),
    )
    return s


def merge_colors(ball_1, ball_2):
    r1, r2 = merge_single(ball_1.color[0], ball_2.color[0])
    g1, g2 = merge_single(ball_1.color[1], ball_2.color[1])
    b1, b2 = merge_single(ball_1.color[2], ball_2.color[2])
    ball_1.color = (r1, g1, b1)
    ball_2.color = (r2, g2, b2)


def merge_single(v1, v2):
    m = (v1 + v2) / 2
    v1 *= 5
    v1 += m
    v1 /= 6

    v2 *= 5
    v2 += m
    v2 /= 6
    return v1, v2


def get_color_list(nbr, cm="cool", return_fmt="int"):
    # https://matplotlib.org/stable/tutorials/colors/colormaps.html
    return cmr.take_cmap_colors(cm, nbr, return_fmt=return_fmt)
    # cool viridis


def create_grid_surface(px_panel_size, px_tile_size, color, alpha=25, type="lines"):
    px_surface_size = px_panel_size + Vector2(px_tile_size, px_tile_size)
    grid_surface = pygame.Surface(px_surface_size.to_tuple(), pygame.SRCALPHA)
    grid_surface.set_alpha(alpha)
    if type == "lines":
        for y in range(px_tile_size, px_surface_size.y, px_tile_size):
            pygame.draw.line(grid_surface, color, (0, y), (px_surface_size.x, y))
        for x in range(px_tile_size, px_surface_size.x, px_tile_size):
            pygame.draw.line(grid_surface, color, (x, 0), (x, px_surface_size.y))
    elif type == "dots":
        for y in range(1, config.t_size.y):
            for x in range(1, config.t_size.x):
                pygame.draw.circle(
                    grid_surface,
                    color=color,
                    center=(Vector2(y=y, x=x) * px_tile_size).to_int_tuple(),
                    radius=int(config.balls_radius / 20),
                    width=0,
                )
    return grid_surface
