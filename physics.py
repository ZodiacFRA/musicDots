import math

import pygame
import numpy as np

import config
import display_utils
from Vector2 import Vector2


def process_borders_collisions(ball, px_window_size):
    is_colliding = False
    if ball.pos.x - ball.radius < 0:
        ball.pos.x = ball.radius
        ball.velocity.x *= -1
        is_colliding = True
    elif ball.pos.x + ball.radius > px_window_size.x:
        ball.pos.x = px_window_size.x - ball.radius
        ball.velocity.x *= -1
        is_colliding = True

    if ball.pos.y - ball.radius < 0:
        ball.pos.y = ball.radius
        ball.velocity.y *= -1
        is_colliding = True
    elif ball.pos.y + ball.radius > px_window_size.y:
        ball.pos.y = px_window_size.y - ball.radius
        ball.velocity.y *= -1
        is_colliding = True

    if is_colliding:
        ball.velocity *= config.dampening_factor
        if config.quantize_position:
            ball.align_to_grid(config.balls_radius)
    return is_colliding


def process_wall_collision(wall, ball, detection_only=False):
    # in the box?
    vec_test_1 = ball.pos - wall.p1
    vec_test_2 = ball.pos - wall.p2
    vec_dot_1 = wall.center_p1.dot(vec_test_1)
    vec_dot_2 = wall.center_p2.dot(vec_test_2)
    # at radius length?
    vec_center_test = ball.pos - wall.center
    center_dot = wall.normal.dot(vec_center_test)
    if vec_dot_1 > 0 and vec_dot_2 > 0 and abs(center_dot) < ball.radius:
        if not detection_only:
            separate_ball_from_wall(ball, wall, center_dot)
            apply_wall_collision(ball, wall, center_dot)
            ball.wall_collisions_count += 1
        return True
    else:
        return False


def separate_ball_from_wall(ball, wall, center_dot):
    """Move the ball so that it does not intersect with the wall
    (as the balls can go too far depending on the simulation resolution)"""
    dr = ball.radius - center_dot
    ball.pos = ball.pos + wall.normal * dr


def apply_wall_collision(ball, wall, center_dot):
    # Change the ball velocity
    tmp = wall.normal * ball.velocity.dot(wall.normal)
    ball.velocity = ball.velocity - tmp * 2
    # Dampening
    ball.velocity *= ball.bounciness * config.dampening_factor


def process_ball_collision(
    ball_1, ball_2, use_mass, detection_only=False, radius_ratio=1
):
    """
    https://stackoverflow.com/questions/345838/ball-to-ball-collision-detection-and-handling
    TODO: While I do agree that the balls hit when the distance is the sum of their radii
    one should never actually calculate this distance!
    Rather, calculate it's square and work with it that way.
    There's no reason for that expensive square root operation.
    """
    collision = ball_1.pos - ball_2.pos
    distance = collision.length()
    balls_overlap = (ball_1.radius + ball_2.radius) / radius_ratio - distance
    if balls_overlap >= 0:
        if not detection_only:
            separate_balls(ball_1, ball_2, balls_overlap, collision)
            apply_ball_collision(ball_1, ball_2, distance, collision, use_mass)
            ball_1.ball_collisions_count += 1
            ball_2.ball_collisions_count += 1
            if config.merge_colors:
                display_utils.merge_colors(ball_1, ball_2)
        return True
    else:
        return False


def separate_balls(ball_1, ball_2, balls_overlap, collision):
    # Remove the 1st ball from the 2nd ball
    dr = collision.normalize() * balls_overlap
    dr /= 2
    ball_1.pos += dr
    ball_2.pos -= dr


def apply_ball_collision(ball_1, ball_2, distance, collision, use_mass):
    if use_mass:
        # Approximate mass transfer
        total_mass = ball_1.mass + ball_2.mass
        new_v1 = (
            ball_1.velocity * (ball_1.mass - ball_2.mass)
            + ball_2.velocity * ball_2.mass * 2
        ) / total_mass
        new_v2 = (
            ball_2.velocity * (ball_2.mass - ball_1.mass)
            + ball_1.velocity * ball_1.mass * 2
        ) / total_mass

        ball_1.velocity = new_v1
        ball_2.velocity = new_v2
    else:
        # Get the components of the velocity vectors which are parallel to the collision.
        # The perpendicular component remains the same for both fish
        collision = collision / distance
        ball_1_ci = ball_1.velocity.dot(collision)
        ball_2_ci = ball_2.velocity.dot(collision)
        ball_1_cf = ball_2_ci
        ball_2_cf = ball_1_ci
        # # Replace the collision velocity components with the new ones
        ball_1.velocity += collision * (ball_1_cf - ball_1_ci) * config.dampening_factor
        ball_2.velocity += collision * (ball_2_cf - ball_2_ci) * config.dampening_factor
