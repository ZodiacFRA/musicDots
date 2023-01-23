""" https://www.youtube.com/shorts/MzVcBnxSHz4 """
import random

import pygame

import init
import display_utils
import config
from physics import *
from Vector2 import *
from Audio import Audio


class App(object):
    def __init__(self):
        if config.seed >= 0:
            random.seed(config.seed)
            print("[ ] - Seed:", config.seed)
        else:
            seed = random.randint(-1000, 1000)
            random.seed(seed)
            print("[ ] - Seed:", seed)
        ### Sound
        self.audio = Audio()
        # Graphics
        self.color_list = display_utils.get_color_list(config.balls_nbr, "cool")
        self.px_window_size = config.t_size * config.balls_radius
        # Create a semi transparent surface which will be blit each time, without screen reset
        # which will create a trail effect
        self.black_fadeout_surface = display_utils.create_surface(
            self.px_window_size, 1
        )
        self.persistant_surface = display_utils.create_surface(self.px_window_size, 255)
        self.grid_surface = display_utils.create_grid_surface(
            self.px_window_size,
            config.balls_radius,
            color="#ffffff",
            alpha=30,
            type="dots",
        )
        ### FPS
        self.elapsed_ticks = 0
        self.fps = 60
        self.clock = pygame.time.Clock()
        ### Pygame
        pygame.init()
        pygame.display.set_caption("Bouncy")
        self.display = pygame.display.set_mode(self.px_window_size.to_int_tuple())
        ### Simulation
        self.walls = init.walls(self.px_window_size)
        self.balls = init.balls(
            self.walls,
            self.px_window_size,
            self.color_list,
        )
        if len(self.balls) <= 1:
            config.balls_nbr = len(self.balls)
        self.dots = init.dots(self.color_list)
        self.rotators = []

    def launch(self):
        while self.handle_loop():
            if config.gravity_rotation_speed:
                config.gravity = config.gravity.rotate(config.gravity_rotation_speed)
            # Update positions
            for idx_ball_1, ball_1 in enumerate(self.balls):
                self.update_ball(idx_ball_1, ball_1)
            self.draw()

    def update_ball(self, idx_ball_1, ball_1):
        ball_1.velocity += config.gravity * config.sim_resolution
        ball_1.update(config.sim_resolution)
        # Check boundaries collisions
        if process_borders_collisions(ball_1, self.px_window_size):
            self.audio.play(ball_1.id, 0)
            pass
        # Wall collisions
        if self.walls:
            for wall in self.walls:
                if process_wall_collision(wall, ball_1):
                    if config.play_wall_collide_sounds:
                        self.audio.play(ball_1.id, 1)
        # Check and apply collisions with the other balls
        if config.collide_balls and config.balls_nbr > 1:
            for ball_2 in self.balls[idx_ball_1 + 1 :]:
                if process_ball_collision(
                    ball_1, ball_2, use_mass=False, radius_ratio=4
                ):
                    if config.play_ball_collide_sounds:
                        self.audio.play(ball_1.id, 2)
                        self.audio.play(ball_2.id, 2)
        # With points
        to_be_removed_dots = set()
        for dot in self.dots:
            if process_ball_collision(
                ball_1, dot, False, detection_only=True, radius_ratio=3
            ):
                to_be_removed_dots.add(dot)
                self.audio.play(ball_1.id, 3)
        for dot in to_be_removed_dots:
            self.dots.remove(dot)
        # With rotators
        for rotator in self.rotators:
            if process_ball_collision(
                ball_1, rotator, detection_only=True, radius_ratio=3
            ):
                ball_1.rotator = rotator

    def draw(self):
        self.display.fill((0, 0, 0, 255))
        for dot in self.dots:
            dot.draw(self.persistant_surface)
        for ball in self.balls:
            ball.draw(self.persistant_surface)

        if config.display_mode == 2:
            if not self.elapsed_ticks % config.fade_slowness:
                self.persistant_surface.blit(self.black_fadeout_surface, (0, 0))
        self.display.blit(self.persistant_surface, (0, 0))
        if config.draw_grid:
            self.display.blit(self.grid_surface, (0, 0))

        for wall in self.walls:
            wall.draw(self.display)
        if config.draw_cursor:
            self.draw_cursor()

    def draw_cursor(self):
        px_cursor_pos = (
            Vector2(*pygame.mouse.get_pos())
            + Vector2(config.balls_radius, config.balls_radius) / 2
        )
        px_cursor_pos = (px_cursor_pos // config.balls_radius) * config.balls_radius
        pygame.draw.circle(
            self.display,
            color=self.color_list[0],
            center=px_cursor_pos.to_int_tuple(),
            radius=int(config.balls_radius / 2),
            width=1,
        )

    def handle_loop(self, debug=False):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ ] - App: Stopping")
                pygame.quit()
                return 0
        self.clock.tick(self.fps)
        self.elapsed_ticks += 1
        return 1


if __name__ == "__main__":
    app = App()
    app.launch()
