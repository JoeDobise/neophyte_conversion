from os import path as _o_path
from sys import path as _s_path
file_dir = _o_path.dirname(__file__)
_s_path.append(file_dir)

# pylint: disable=wrong-import-position
from base_types import AudioFileType, WaveFileType, WaveFile  # noqa: E402


class PolyendTrackerSampleType(WaveFileType):
    """
    Class type for Polyend Tracker Sample, can be mono 16/24/32 bit
    Sample rate needs to be 44.1khz
    Default bit depth is set to 24 bit

    Instantiate an 16 bit object in the following way
    >>> test=OctatrackSampleType(16)
    """

    def __init__(self, default_bit_depth=24):
        super().__init__(
            name="Polyend Tracker Sample",
            short_name="track",
            sample_rate=44100,
            bit_depth={16, 24, 32},
        )
        self.set_default_sample_rate(44100)
        self.set_default_bit_depth(default_bit_depth)


class PolyendTrackerSample(WaveFile):
    """Sample file that is compliant with Polyend Tracker"""

    def __init__(
        self,
        file_path,
        file_type: AudioFileType = PolyendTrackerSampleType,
        bit_depth: int = 24,
        channel_count: int = 1,
    ) -> None:
        super().__init__(
            file_path=file_path,
            file_type=file_type,
            bit_depth=bit_depth,
            channel_count=channel_count,
        )
