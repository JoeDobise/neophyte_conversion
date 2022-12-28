from os import path as _o_path
from sys import path as _s_path
file_dir = _o_path.dirname(__file__)
_s_path.append(file_dir)

# pylint: disable=wrong-import-position
from base_types import AudioFileType, WaveFileType, WaveFile  # noqa: E402


class RampleSampleType(WaveFileType):
    """
    Class type for Rample Sample, can be mono 8 or 16 bit
    Sample rate needs to be 44.1khz
    Default bit depth is set to 16 bit

    Instantiate an 8 bit object in the following way
    >>> test=OctatrackSampleType(8)
    """

    def __init__(self, default_bit_depth=16):
        super().__init__(
            name="Rample Sample",
            short_name="rample",
            sample_rate=44100,
            bit_depth={8, 16},
        )
        self.set_default_sample_rate(44100)
        self.set_default_bit_depth(default_bit_depth)


class RampleSample(WaveFile):
    """Sample file that is compliant with Squarp Rample"""

    def __init__(
        self,
        file_path,
        file_type: AudioFileType = RampleSampleType,
        bit_depth: int = 16,
        channel_count: int = 1,
    ) -> None:
        super().__init__(
            file_path=file_path,
            file_type=file_type,
            bit_depth=bit_depth,
            channel_count=channel_count,
        )
