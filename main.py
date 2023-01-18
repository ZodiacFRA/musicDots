""" https://www.youtube.com/shorts/MzVcBnxSHz4 """
import random

import pygame

import utils
import config
from physics import *
from Vector2 import *
from Audio import Audio


class App(object):
    def __init__(self):
        random.seed(42)
        ### Sound
        self.audio = Audio()
        # Graphics
        self.px_window_size = Vector2(1024, 1024)
        # Create a semi transparent surface which will be blit each time, without screen reset
        # which will create a trail effect
        self.alpha_curtain = pygame.Surface(
            self.px_window_size.to_int_tuple(), pygame.SRCALPHA
        )
        self.alpha_curtain.set_alpha(1)
        pygame.draw.rect(
            self.alpha_curtain,
            (0, 0, 0),
            pygame.Rect(0, 0, *self.px_window_size.to_int_tuple()),
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
        self.walls = [
            Wall(Vector2(self.px_window_size.x, 0), Vector2(0, 0)),
            Wall(
                Vector2(self.px_window_size.x, self.px_window_size.y),
                Vector2(self.px_window_size.x, 0),
            ),
            Wall(
                Vector2(0, self.px_window_size.y),
                Vector2(self.px_window_size.x, self.px_window_size.y),
            ),
            Wall(Vector2(0, 0), Vector2(0, self.px_window_size.y)),
            ##
            # Wall(Vector2(50, 800), Vector2(500, 900)),
            # Wall(Vector2(500, 900), Vector2(700, 20)),
            # Wall(Vector2(700, 20), Vector2(20, 20)),
            # Wall(Vector2(20, 20), Vector2(50, 800)),
        ]
        self.balls = utils.init_balls(
            20, self.walls, self.px_window_size, self.audio.get_bank_len("perc")
        )
        random.shuffle(self.balls)

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
            pygame.display.update()

    def draw(self):
        for ball in self.balls:
            ball.draw(self.display)
        for wall in self.walls:
            wall.draw(self.display)

    def handle_loop(self, debug=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ ] - App: Stopping")
                pygame.quit()
                return 0
        self.clock.tick(self.fps)

        if config.display_mode == 1:
            self.display.fill((0, 0, 0, 255))
        elif config.display_mode == 2:
            if not self.elapsed_ticks % config.fade_slowness:
                self.display.blit(self.alpha_curtain, (0, 0))
        self.elapsed_ticks += 1
        return 1


if __name__ == "__main__":
    app = App()
    app.launch()
