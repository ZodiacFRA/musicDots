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


def get_scale_notes_indexes(offset=0, scale_name="minor", max_nbr=0):
    """if max_nbr == 0: do not add other octaves to the scale"""
    # Transform the intervals into indexes
    note = config.named_scales[scale_name][0]
    scale = [0, note]
    for interval in config.named_scales[scale_name][1:]:
        scale.append(interval + note)
        note += interval
    scale = [n + offset for n in scale]
    if max_nbr == 0:
        return scale
    repeated_scale = scale
    while len(repeated_scale) < max_nbr:
        repeated_scale += [n + 12 for n in scale]
    return repeated_scale
