""" https://www.youtube.com/shorts/MzVcBnxSHz4 """
import random

import pygame

import init
import utils
import display_utils
import config
from physics import *
from Vector2 import *
from Audio import Audio


class App(object):
    def __init__(self):
        if config.seed >= 0:
            random.seed(config.seed)
        ### Sound
        self.audio = Audio()
        # Graphics
        self.color_list = display_utils.get_color_list(config.balls_nbr, "cool")
        self.px_window_size = config.t_size * config.balls_radius
        # Create a semi transparent surface which will be blit each time, without screen reset
        # which will create a trail effect
        self.black_fadeout_surface = display_utils.create_occlusion_surface(
            self.px_window_size, 1
        )
        self.grid_surface = display_utils.create_grid_surface(
            self.px_window_size, config.balls_radius, color="#000000"
        )
        ### FPS
        self.elapsed_ticks = 0
        self.fps = 120
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
        self.dots = init.dots(self.balls, self.walls, self.color_list)

    def launch(self):
        while self.handle_loop():
            # Update positions
            to_be_removed_dots = set()
            for idx_ball_1, ball_1 in enumerate(self.balls):
                ball_1.velocity += config.gravity * config.sim_resolution
                ball_1.update(config.sim_resolution)
                # Check boundaries collisions
                if process_borders_collisions(ball_1, self.px_window_size):
                    self.audio.play(ball_1, "piano")
                    pass
                # Wall collisions
                if self.walls:
                    for wall in self.walls:
                        if process_wall_collision(wall, ball_1):
                            if config.play_wall_collide_sounds:
                                self.audio.play(ball_1)
                # Check and apply collisions with the other balls
                if config.collide_balls and config.balls_nbr > 1:
                    for ball_2 in self.balls[idx_ball_1 + 1 :]:
                        if process_ball_collision(
                            ball_1, ball_2, use_mass=False, radius_ratio=4
                        ):
                            if config.play_ball_collide_sounds:
                                self.audio.play(ball_1)
                                self.audio.play(ball_2)
                # With points
                for dot_idx, dot in enumerate(self.dots):
                    if process_ball_collision(
                        ball_1, dot, False, detection_only=True, radius_ratio=3
                    ):
                        to_be_removed_dots.add(dot_idx)
                        self.audio.play(ball_1, "perc")

            to_be_removed_dots = list(to_be_removed_dots)
            to_be_removed_dots.sort(reverse=True)
            for dot_idx in to_be_removed_dots:
                self.dots.pop(dot_idx)

            self.draw()
            if config.gravity_rotation_speed:
                config.gravity = config.gravity.rotate(config.gravity_rotation_speed)

    def draw(self):
        if config.draw_grid:
            self.draw_grid()
        for dot in self.dots:
            dot.draw(self.display)
        for ball in self.balls:
            ball.draw(self.display)
        for wall in self.walls:
            wall.draw(self.display)

    def draw_grid(self):
        self.display.blit(self.grid_surface, (0, 0))

    def handle_loop(self, debug=False):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ ] - App: Stopping")
                pygame.quit()
                return 0
        self.clock.tick(self.fps)
        self.apply_display_mode()
        self.elapsed_ticks += 1
        return 1

    def apply_display_mode(self):
        if config.display_mode == 1:
            self.display.fill((0, 0, 0, 255))
        elif config.display_mode == 2:
            if not self.elapsed_ticks % config.fade_slowness:
                self.display.blit(self.black_fadeout_surface, (0, 0))


if __name__ == "__main__":
    app = App()
    app.launch()
