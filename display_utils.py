import pygame
import cmasher as cmr


def create_occlusion_surface(px_window_size, alpha_value):
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
