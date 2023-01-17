import time
import random

import pygame
import cmasher as cmr

import config
from physics import *
from Vector2 import *


class App(object):
    def __init__(self):
        ### Sound
        pygame.mixer.init()
        pygame.mixer.set_num_channels(20)
        self.samples = []
        self.filepath_list = [f"./samples/{n + 1:03}.wav" for n in range(67)]
        for filepath in self.filepath_list:
            tmp = pygame.mixer.Sound(filepath)
            tmp.set_volume(0.2)
            self.samples.append(tmp)
        self.samples = self.samples[24:]
        # Graphics
        self.color_list = cmr.take_cmap_colors("viridis", 4, return_fmt="hex")
        self.px_window_size = Vector2(1000, 1000)
        ### FPS
        self.fps = 240
        self.clock = pygame.time.Clock()
        ### Pygame
        pygame.init()
        pygame.display.set_caption("Bouncy")
        self.display = pygame.display.set_mode(self.px_window_size.to_int_tuple())
        ### Simulation
        self.balls = [
            Ball(
                pos=Vector2(40, 40),
                velocity=Vector2(400, 0),
                bounciness=1,
                radius=10,
                color=self.color_list[0],
                sound_idx=0,
            ),
            Ball(
                pos=Vector2(100, 100),
                velocity=Vector2(0, 400),
                bounciness=1,
                radius=20,
                color=self.color_list[1],
                sound_idx=4,
            ),
            Ball(
                pos=Vector2(250, 250),
                velocity=Vector2(0, 400),
                bounciness=1,
                radius=30,
                color=self.color_list[2],
                sound_idx=8,
            ),
            Ball(
                pos=Vector2(500, 500),
                velocity=Vector2(100, 700),
                bounciness=1,
                radius=50,
                color=self.color_list[3],
                sound_idx=11,
            ),
        ]
        self.walls = [
            Wall(Vector2(50, 800), Vector2(500, 900)),
            Wall(Vector2(500, 900), Vector2(700, 20)),
            Wall(Vector2(700, 20), Vector2(20, 20)),
            Wall(Vector2(20, 20), Vector2(50, 800)),
        ]

    def __del__(self):
        pygame.mixer.quit

    def launch(self):
        while self.handle_loop():
            # Update positions
            for idx, ball in enumerate(self.balls):
                ball.velocity += config.gravity * config.sim_resolution
                ball.update(config.sim_resolution)
                # Check and apply collisions with the walls
                for wall in self.walls:
                    if process_wall_collision(wall, ball):
                        self.samples[len(self.samples) - 1].play()
                        # pygame.mixer.Channel(idx).play(self.samples[idx])
                # Check and apply collisions with the other balls
                for idx_2, ball_2 in enumerate(self.balls[idx + 1 :]):
                    if process_ball_collision(ball, ball_2):
                        self.samples[ball.sound_idx].play()
                        self.samples[ball_2.sound_idx].play()
            self.draw()
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
        self.display.fill("#000000")
        return 1


if __name__ == "__main__":
    app = App()
    app.launch()
