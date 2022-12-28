#!/usr/bin/python3


from audio_types import AudioFileType, WaveFileType, WaveFile


class OctatrackSampleType(WaveFileType):
    """
    Class type for Octatrack Samples, can be 16 or 24 bit
    Sample rate needs to be 44.1khz
    Default bit depth is set to 24 bit

    Instantiate a 16 bit object in the following way
    >>> test=OctatrackSampleType(16)
    """

    def __init__(self, default_bit_depth=24):
        super().__init__(
            name="Octatrack Sample",
            short_name="octa",
            sample_rate=44100,
            bit_depth={16, 24},
        )
        self.set_default_sample_rate(44100)
        self.set_default_bit_depth(default_bit_depth)


class OctatrackSample(WaveFile):
    """Sample file that is compliant with Octatrack"""

    def __init__(
        self,
        file_path,
        file_type: AudioFileType = OctatrackSampleType,
        bit_depth: int = 24,
    ) -> None:
        super().__init__(
            file_path=file_path,
            file_type=file_type,
            bit_depth=bit_depth,
        )