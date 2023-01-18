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
        self.px_window_size = Vector2(1024, 512)
        # Create a semi transparent surface which will be blit each time, without screen reset
        # which will create a trail effect
        self.black_fadeout_surface = display_utils.create_occlusion_surface(
            self.px_window_size, 1
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
            5, self.walls, self.px_window_size, self.audio.get_bank_len("piano")
        )
        self.dots = init.dots(self.px_window_size)

    def launch(self):
        while self.handle_loop():
            # Update positions
            for idx, ball in enumerate(self.balls):
                ball.velocity += config.gravity * config.sim_resolution
                ball.update(config.sim_resolution)
                # Check and apply collisions with the walls
                for wall in self.walls:
                    if process_wall_collision(wall, ball):
                        if config.play_wall_collide_sounds:
                            self.audio.play(ball)
                if config.collide_balls:
                    # Check and apply collisions with the other balls
                    for ball_2 in self.balls[idx + 1 :]:
                        if process_ball_collision(ball, ball_2, use_mass=False):
                            if config.play_ball_collide_sounds:
                                self.audio.play(ball)
                                self.audio.play(ball_2)
                if ball.velocity.simple_length() < config.stable_treshold:
                    ball.velocity /= 10
            self.draw()
            if config.gravity_rotation_speed:
                config.gravity = config.gravity.rotate(config.gravity_rotation_speed)

    def draw(self):
        for ball in self.balls:
            ball.draw(self.display)
        for wall in self.walls:
            wall.draw(self.display)

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
