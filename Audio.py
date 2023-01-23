""" 
https://spotify.github.io/pedalboard/reference/pedalboard.html#pedalboard.Phaser
https://github.com/spotify/pedalboard
"""
import os
import random

import pygame
import numpy as np
from tqdm import tqdm
from pedalboard import *

import utils
import config
import audio_utils


class Audio(object):
    def __init__(self):
        self.samplerate = 44100.0
        self.notes = audio_utils.get_scale_notes_indexes(
            scale_name="minor", offset=42, max_nbr=config.balls_nbr * 3
        )
        ### Pygame
        pygame.mixer.init()
        pygame.mixer.set_num_channels(50)
        ### Pedalboard processing
        if config.process_samples:
            self.repitch_dir("./samples/perc")
            self.add_effects_to_dir("./samples/piano")
        ### Data
        self.samples = {
            "piano": audio_utils.load_sample_dir("./samples/piano"),
            "perc": audio_utils.load_sample_dir("./samples/perc"),
        }

    def play(self, id, collision_type):
        if not config.use_sound:
            return
        if collision_type == 0:
            sample = self.samples["piano"][self.notes[id]]
        elif collision_type == 1:
            sample = self.samples["piano"][self.notes[id]]
        elif collision_type == 2:
            sample = self.samples["piano"][self.notes[id]]
        else:
            sample = self.samples["perc"][1]
        # sample.set_volume(ball.velocity.artistic_velocity() / 80000)
        sample.play()

    def add_effects_to_dir(self, dir_path):
        board = Pedalboard(
            [
                Compressor(threshold_db=-25, ratio=25),
                Gain(gain_db=10),
                Chorus(),
                Phaser(rate_hz=0.1),
                Reverb(room_size=0.2),
            ]
        )
        for sample_path in tqdm(utils.get_filepaths_from_dir(dir_path)):
            self.add_effect_to_sample(sample_path, board)

    def add_effect_to_sample(self, sample_path, board):
        sample = audio_utils.load_sample_to_np_array(sample_path, self.samplerate)
        processed_sample_path = os.path.join(
            dir_path, "processed/", os.path.basename(sample_path)
        )
        processed_sample = board(sample, self.samplerate)
        audio_utils.write_sample(
            processed_sample_path, processed_sample, self.samplerate
        )
        # Animate board params
        board[3].depth = random.randint(0, 100) / 100
        board[3].rate_hz = random.randint(0, 20) / 10

    def repitch_dir(self, dir_path):
        for sample_path in tqdm(utils.get_filepaths_from_dir(dir_path)):
            sample = audio_utils.load_sample_to_np_array(sample_path, self.samplerate)
            self.create_repitched_versions_of_sample(sample, sample_path, dir_path)

    def create_repitched_versions_of_sample(self, sample, sample_path, dir_path):
        board = Pedalboard([PitchShift(semitones=0)])
        for semitone in config.repitch_scale:
            processed_sample_path = os.path.join(
                dir_path, "processed/", semitone, os.path.basename(sample_path)
            )
            processed_sample = board(sample, self.samplerate)
            audio_utils.write_sample(
                processed_sample_path, processed_sample, self.samplerate
            )
            # Animate board params
            board[0].semitones = semitone

    def get_bank_len(self, bank):
        return len(self.samples[bank])

    def __del__(self):
        pygame.mixer.quit
