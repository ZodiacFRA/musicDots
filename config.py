from Vector2 import Vector2

### App
seed = -1
# Simulation
t_size = Vector2(32, 18)
inital_ball_nbr = 1
balls_nbr = 15

balls_radius = 32
dampening_factor = 1
gravity = Vector2(0, 0)
gravity_rotation_speed = 0  # 0.0005
sim_resolution = 1
stable_treshold = 10  # in pixels length not sqrt (big values)
quantize_position = True
collide_balls = False
# Graphics
display_mode = 2
fade_slowness = 1
merge_colors = True
draw_grid = True
draw_cursor = False

### Audio
use_sound = False
base_volume = 0.1
play_wall_collide_sounds = True
play_ball_collide_sounds = False
# Samples
process_samples = False
# Musical
named_scales = {
    "major": (2, 2, 1, 2, 2, 2, 1),
    "minor": (2, 1, 2, 2, 1, 2, 2),
    "melodicminor": (2, 1, 2, 2, 2, 2, 1),
    "harmonicminor": (2, 1, 2, 2, 1, 3, 1),
    "pentatonicmajor": (2, 2, 3, 2, 3),
    "bluesmajor": (3, 2, 1, 1, 2, 3),
    "pentatonicminor": (3, 2, 2, 3, 2),
    "bluesminor": (3, 2, 1, 1, 3, 2),
    "augmented": (3, 1, 3, 1, 3, 1),
    "diminished": (2, 1, 2, 1, 2, 1, 2, 1),
    "chromatic": (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    "wholehalf": (2, 1, 2, 1, 2, 1, 2, 1),
    "halfwhole": (1, 2, 1, 2, 1, 2, 1, 2),
    "wholetone": (2, 2, 2, 2, 2, 2),
    "augmentedfifth": (2, 2, 1, 2, 1, 1, 2, 1),
    "japanese": (1, 4, 2, 1, 4),
    "oriental": (1, 3, 1, 1, 3, 1, 2),
    "ionian": (2, 2, 1, 2, 2, 2, 1),
    "dorian": (2, 1, 2, 2, 2, 1, 2),
    "phrygian": (1, 2, 2, 2, 1, 2, 2),
    "lydian": (2, 2, 2, 1, 2, 2, 1),
    "mixolydian": (2, 2, 1, 2, 2, 1, 2),
    "aeolian": (2, 1, 2, 2, 1, 2, 2),
    "locrian": (1, 2, 2, 1, 2, 2, 2),
}
scale = "harmonicminor"
