""" 
https://spotify.github.io/pedalboard/reference/pedalboard.html#pedalboard.Phaser
https://github.com/spotify/pedalboard
"""
import os
import random

import numpy as np
from tqdm import tqdm
import pygame
from pedalboard import *
from pedalboard.io import AudioFile

import config


class Audio(object):
    def __init__(self):
        self.samplerate = 44100.0
        ### Pygame
        pygame.mixer.init()
        pygame.mixer.set_num_channels(50)
        ### Pedalboard
        self.board = Pedalboard(
            [
                PitchShift(semitones=0),
                # Compressor(threshold_db=-25, ratio=25),
                # Gain(gain_db=10),
                # Chorus(),
                # Phaser(rate_hz=0.1),
                # Reverb(room_size=0.2),
            ]
        )
        ### Data
        self.samples = {
            "piano": self.load_folder("./samples/piano", process=False),
            # "piano": self.load_folder("./samples/piano", process=True),
            # "perc": self.load_folder("./samples/perc", process=True, repitch=True),
            "perc": self.load_folder(
                "./samples/perc/processed", process=False, repitch=True
            ),
        }

    def load_folder(self, folderpath, process=True, repitch=False):
        samples = []
        # file_list = [f"{n + 1:03}.wav" for n in range(67)]
        file_list = [file for file in os.listdir(folderpath) if file.endswith(".wav")]
        print(folderpath, file_list)
        sample_path_list = []
        for file in tqdm(file_list):
            out_path = folderpath + "/processed/"

            if process:
                # self.board[4].depth = random.randint(0, 100) / 100
                # self.board[4].rate_hz = random.randint(0, 20) / 10
                with AudioFile(f"{folderpath}/{file}").resampled_to(
                    self.samplerate
                ) as f:
                    audio = f.read(f.frames)
                # Write the original
                self.board[0].semitones = 0
                effected = self.board(audio, self.samplerate)
                with AudioFile(
                    f"{out_path}0_{file}",
                    "w",
                    self.samplerate,
                    effected.shape[0],
                ) as f:
                    f.write(effected)
                    sample_path_list.append(f"{out_path}0_{file}")
                if repitch:
                    for semitone in [0, 3, 5, 6, 7, 12, 15, 17, 18, 19, 24]:
                        self.board[0].semitones = semitone
                        # Run the audio through this pedalboard!
                        effected = self.board(audio, self.samplerate)
                        with AudioFile(
                            f"{out_path}{semitone}_{file}",
                            "w",
                            self.samplerate,
                            effected.shape[0],
                        ) as f:
                            f.write(effected)
                            sample_path_list.append(f"{out_path}{semitone}_{file}")

        target = sample_path_list if process else file_list
        for sample_path in target:
            tmp = pygame.mixer.Sound(f"{folderpath}/{sample_path}")
            tmp.set_volume(config.base_volume)
            samples.append(tmp)
        return samples

    def play(self, ball, bank="perc"):
        sample = self.samples[bank][ball.get_sample_idx(len(self.samples[bank]))]
        # sample.set_volume(ball.velocity.artistic_velocity() / 80000)
        sample.play()

    def get_bank_len(self, bank):
        return len(self.samples[bank])

    def __del__(self):
        pygame.mixer.quit
