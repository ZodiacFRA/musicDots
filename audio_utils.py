import pygame
from tqdm import tqdm
from pedalboard.io import AudioFile

import utils
import config


def load_sample_dir(dirpath):
    res = []
    for sample_path in tqdm(utils.get_filepaths_from_dir(dirpath)):
        tmp = pygame.mixer.Sound(sample_path)
        tmp.set_volume(config.base_volume)
        res.append(tmp)
    return res


def load_sample_to_np_array(filepath, samplerate):
    with AudioFile(filepath.resampled_to(samplerate)) as f:
        sample = f.read(f.frames)
    return sample


def write_sample(filepath, data, samplerate):
    with AudioFile(filepath, "w", samplerate, data.shape[0]) as f:
        f.write(data)
