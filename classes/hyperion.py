from os import path as _o_path
from sys import path as _s_path

file_dir = _o_path.dirname(__file__)
_s_path.append(file_dir)

# pylint: disable=wrong-import-position
from base_types import AudioFileType, WaveFileType, WaveFile  # noqa: E402


class HyperionImpulseType(WaveFileType):
    """
    Class type for SynthTech e520 Hyperion Effects Impulse Responses.
    Hyperion IR's only currently work at Mono 16 bit 48khz
    """

    def __init__(self, default_bit_depth=16):
        super().__init__(
            name="Hyperion IR Sample",
            short_name="hyperion",
            sample_rate=48000,
            bit_depth={16},
        )
        self.set_default_sample_rate(48000)
        self.set_default_bit_depth(default_bit_depth)


class HyperionImpulse(WaveFile):
    """
    Sample file that is compliant with Synthesis Technology
    e520 Hyperion Effects Processor
    """

    def __init__(
        self,
        file_path,
        file_type: AudioFileType = HyperionImpulseType,
        bit_depth: int = 16,
        channel_count: int = 1,
    ) -> None:
        super().__init__(
            file_path=file_path,
            file_type=file_type,
            bit_depth=bit_depth,
            channel_count=channel_count,
        )
