import pygame


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
        self.ball_collisions_count = 0
        self.wall_collisions_count = 0

    def update(self, dt):
        self.pos = self.pos + (self.velocity * dt)

    def draw(self, screen):
        color = tuple([min(255, self.velocity.artistic_velocity() / 100)] * 3)
        pygame.draw.circle(
            screen,
            # self.color,
            color,
            # "#ffffff",
            self.pos.to_int_tuple(),
            radius=int(self.radius / 2),
            # radius=self.velocity.ln_range_transform() * 2,
            # radius=int(self.velocity.simple_length() / 1000),
            width=0,
        )

    def get_sample_idx(self, samples_nbr):
        # return (self.sound_idx + 1 * self.wall_collisions_count) % samples_nbr
        return self.sound_idx
