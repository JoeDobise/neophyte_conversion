#!/usr/bin/python3

from os import path as o_path
from classes.audio_types import AudioFile

from helpers import (
    find_all_target_files,
    get_sample_processor,
    compare_file_to_target_sample
)

if __name__ == "__main__":
    directory = o_path.realpath(o_path.curdir)
    sample: str = "octa"

    SampleProcessor: AudioFile = get_sample_processor(sample)
    sample_type = SampleProcessor.file_type()
   
    NERF = True  # removing this line will resample all wave files
    # this is still a work in progress please treat its usage with caution

    target_files = [] if NERF else find_all_target_files(
        directory, 
        sample_type
    )

    for file in target_files:
        if (result := compare_file_to_target_sample(file, SampleProcessor)):
            existing, target = result
            existing.resample_audio_file(target)
