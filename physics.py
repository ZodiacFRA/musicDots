import math

import pygame
import numpy as np

import config


def process_wall_collision(wall, ball):
    # in the box?
    vec_test_1 = ball.pos - wall.p1
    vec_test_2 = ball.pos - wall.p2
    vec_dot_1 = wall.center_p1.dot(vec_test_1)
    vec_dot_2 = wall.center_p2.dot(vec_test_2)
    # at radius length?
    vec_center_test = ball.pos - wall.center
    center_dot = wall.normal.dot(vec_center_test)
    if vec_dot_1 > 0 and vec_dot_2 > 0 and abs(center_dot) < ball.radius:
        # Remove the ball from the wall
        dr = ball.radius - center_dot
        ball.pos = ball.pos + wall.normal * dr
        # Change the ball velocity
        tmp = wall.normal * ball.velocity.dot(wall.normal)
        ball.velocity = ball.velocity - tmp * 2
        # Dampening
        ball.velocity *= ball.bounciness * config.dampening_factor
        return True
    else:
        return False


def process_ball_collision(ball_1, ball_2, use_mass):
    collision = ball_1.pos - ball_2.pos
    # TODO: While I do agree that the balls hit when the distance is the sum of their radii
    # one should never actually calculate this distance!
    # Rather, calculate it's square and work with it that way.
    # There's no reason for that expensive square root operation.
    distance = collision.length()
    balls_overlap = (ball_1.radius + ball_2.radius) - distance
    if balls_overlap >= 0:
        # Remove the 1st ball from the 2nd ball
        dr = collision.normalize() * balls_overlap
        dr /= 2
        ball_1.pos += dr
        ball_2.pos -= dr

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
            ball_1.velocity += (
                collision * (ball_1_cf - ball_1_ci) * config.dampening_factor
            )
            ball_2.velocity += (
                collision * (ball_2_cf - ball_2_ci) * config.dampening_factor
            )
        return True
    else:
        return False


class Wall(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.center = (p1 + p2) / 2

        self.center_p1 = (self.center - self.p1).normalize()
        self.center_p2 = (self.center - self.p2).normalize()

        self.normal = (self.p2 - self.p1).rotate(-1 * math.pi / 2).normalize()

        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.line(
            screen, self.color, self.p1.to_int_tuple(), self.p2.to_int_tuple(), 2
        )


class Ball(object):
    def __init__(
        self,
        pos,
        velocity,
        bounciness=1,
        radius=20,
        color=(255, 255, 255),
        sound_idx=0,
        mass=None,
    ):
        self.radius = radius
        self.mass = radius if mass is None else mass
        self.pos = pos
        self.velocity = velocity
        self.bounciness = bounciness

        self.color = color
        self.sound_idx = sound_idx

    def update(self, dt):
        self.pos = self.pos + (self.velocity * dt)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            self.pos.to_int_tuple(),
            int(self.radius),
            int(self.radius),
        )
