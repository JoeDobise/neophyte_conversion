from os import path as o_path
from os import walk as o_walk
from typing import Optional, Tuple

from classes.base_types import AudioData, AudioFile
from classes.octatrack import OctatrackSample
from classes.rample import RampleSample
from classes.tracker import PolyendTrackerSample


def append_filename_before_extension(
    filename: str,
    addition: str,
    separator: str = "_",
    empty_return_when_present: bool = True,
) -> str:
    """
    Helper function to append file name preserving extension.
        filename: full path to file location
            >>> append_filename_before_extension("/path/to/file.ext", ...
        addition: string to append to filename prior to the extension
            >>> append_filename_before_extension("/path/to/file.ext", "octa")
            result: "/path/to/file_octa.ext"
        separator: string or char to add before addition
            >>> path = "/path/to/file.ext"
            >>> append_filename_before_extension(path, "octa", "*")
            result: "/path/to/file*octa.ext"
        empty_return_when_present: when a filename already ends with addition
            >>> append_filename_before_extension(path, "octa", "_", True)
            result: "" ( this is the default)
            >>> append_filename_before_extension([path], "octa", "_", False)
            result: "/path/to/file_octa_octa.ext"
    """
    addition = separator + addition
    name, extension = o_path.splitext(filename)
    if empty_return_when_present and name.endswith(addition):
        return ""
    return name + addition + extension


def find_all_target_files(
    directory: str,
    file_extensions: set,
) -> list:
    """
    Helper function, to find the absolute path for all files in a given
    directory of a given sample type.
        directory: a path to an existing directory
        sample_type: the sample type to look for
    """
    target_files = []
    if o_path.isdir(directory):
        for root, _, files in o_walk(directory):
            for file in files:
                full_path = o_path.join(root, file)
                if o_path.splitext(full_path)[1] in file_extensions:
                    target_files.append(full_path)
    return target_files


def get_sample_processor(
    sample_type: str,
) -> AudioFile:
    """
    Helper function, to return sample types
    """
    if sample_type == "octa":
        return OctatrackSample
    if sample_type == "tracker":
        return PolyendTrackerSample
    if sample_type == "rample":
        return RampleSample


def generate_input_output_file_metadata(
    file: str,
    proc: AudioFile,
    input_dir: str,
    output_dir: str,
    append_string: Optional[str],
    replace_files: bool = False,
) -> Tuple[AudioFile, AudioFile]:
    """
    Helper function, to handle conversion decision logic
    """
    existing_file = proc(file)
    existing_file.update_instance_metadata()
    target_file = proc(file)

    if replace_files:
        return existing_file, target_file

    if input_dir != output_dir:
        target_file.file_path = o_path.join(
            output_dir, target_file.file_path.strip(input_dir)
        )

    target_file.file_path = append_filename_before_extension(
        target_file.file_path, append_string
        if append_string
        else target_file.file_type.short_name,
    )
    return existing_file, target_file


def update_target_values(
    target_file: AudioFile,
    sample_rate=None,
    bit_depth=None,
    force_mono=False
) -> AudioData:
    """
    Updates defaults for file type
    """

    return AudioData(
        number_of_channels=1 if force_mono else 0,
        bit_depth=bit_depth if bit_depth else target_file.bit_depth,
        sample_rate=sample_rate
        if sample_rate
        else target_file.sample_rate,
        subtype="n/a"
    )
