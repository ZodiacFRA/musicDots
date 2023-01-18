from Vector2 import Vector2


# Simulation
dampening_factor = 0.9
gravity = Vector2(0, 10)
gravity_rotation_speed = 0.0005
sim_resolution = 0.02
stable_treshold = 10  # in pixels length not sqrt (big values)
collide_balls = True

# Graphics
display_mode = 2
fade_slowness = 1
merge_colors = False
# Audio
base_volume = 0.1
play_wall_collide_sounds = False
play_ball_collide_sounds = True

# scale = [0, 2, 3, 5, 7, 8, 10]
scale = [0, 7]
