from typing import Set, Union, Optional
from dataclasses import dataclass
from os import path as o_path
import wave

STANDARD_BIT_DEPTHS: Set[int] = {8, 16, 24, 32}
STANDARD_BIT_RATE_PER_SECOND_RANGE: Set[int] = {16000, 320000}
STANDARD_SAMPLE_RATES: Set[int] = {8000, 16000, 32000, 44100, 48000, 96000}
WAVEFILE_EXTENSIONS: Set[str] = {".WAVE", ".wave", ".WAV", ".wav"}
MP3_EXTENSIONS: Set[str] = {".mp3", ".MP3"}


class AudioFileType:
    """Base class for Audio File Types"""

    def __init__(
        self,
        name: str,
        extension: Union[str, Set[str]],
        short_name: str = None,
        sample_rate: Union[int, Set[int]] = None,
    ):
        self.name = name
        # Set a short name to be used if file is
        self.short_name = (
            short_name
            if short_name
            else name.split()[0][:4].lower()
        )
        if extension:
            self.extensions = (
                {extension}
                if isinstance(extension, str)
                else extension
            )
            self._default_extension = min(self.extensions).lower()
        else:
            raise ValueError(
                f"No extensions were provided for AudioFileType {name}"
            )
        self.sample_rates = (
            {sample_rate}
            if isinstance(sample_rate, str)
            else sample_rate
            if isinstance(sample_rate, set)
            else STANDARD_SAMPLE_RATES
        )
        self._default_sample_rate = max(self.sample_rates)

    def __str__(self):
        attributes = [
            f"  {k} = '{v}'\n"
            for k, v
            in self.__dict__.items() if k[0] != '_'
        ]
        return (
            f"{self.__class__.__name__}\n{''.join(attributes)}"
        )

    def __repr__(self):
        attributes = [
            f"{k}='{v}'"
            for k, v
            in self.__dict__.items()
            if k[0] != '_'
        ]
        private_attributes = [
            f"{k}='{v}'"
            for k, v
            in self.__dict__.items()
            if k[0] == '_'
        ]
        return (
            f"<{self.__class__.__name__} "
            f"{' '.join(attributes)} {' '.join(private_attributes)} >"
        )

    def set_default_extension(self, extension: str) -> None:
        """Sets the private default extension value"""
        if extension not in self.extensions:
            self.extensions = self.extensions.union({extension})
        self._default_extension = extension

    def get_default_extension(self) -> str:
        """Provides private default extension value"""
        return self._default_extension

    def get_extensions(self) -> set[str]:
        """Provides a set of available extensions"""
        return self.extensions

    def set_default_sample_rate(self, sample_rate: int) -> None:
        """Sets the private default sample rate value"""
        if sample_rate not in self.sample_rates:
            self.sample_rates = self.sample_rates.union({sample_rate})
        self._default_sample_rate = sample_rate

    def get_default_sample_rate(self) -> int:
        """Provides private default sample rate value"""
        return self._default_sample_rate


class WaveFileType(AudioFileType):
    """Standard class for Wave File Type"""

    def __init__(
        self,
        name: str = None,
        short_name: str = None,
        extension: Union[str, Set[str]] = None,
        bit_depth: Union[int, Set[int]] = None,
        sample_rate: Union[int, Set[int]] = None,
        channel_count: int = None,
    ):
        super().__init__(
            name=name if name else "Wave File",
            short_name=short_name if short_name else "wav",
            extension=(
                {extension}
                if isinstance(extension, str)
                else extension
                if isinstance(extension, set)
                else WAVEFILE_EXTENSIONS
            ),
            sample_rate=(
                {sample_rate} if isinstance(sample_rate, int) else sample_rate
            ),
        )
        self.bit_depths = (
            {bit_depth}
            if isinstance(bit_depth, int)
            else bit_depth
            if isinstance(bit_depth, set)
            else STANDARD_BIT_DEPTHS
        )
        self.channel_count = channel_count if channel_count else 2
        self._default_channel_count = 2
        self._default_bit_depth = 24
        self.set_default_sample_rate(48000)
        self.set_default_extension(".wav")

    def set_default_bit_depth(self, bit_depth: int) -> None:
        """Sets the private default bit_depth value"""
        if bit_depth not in self.bit_depths:
            self.bit_depths = self.bit_depths.union({bit_depth})
        self._default_bit_depth = bit_depth

    def get_default_bit_depth(self) -> int:
        """Provides private default bit depth value"""
        return self._default_bit_depth

    def set_default_channel_count(self, channel_count: int) -> None:
        """Sets the private default bit_depth value"""
        self._default_channel_count = channel_count

    def get_default_channel_count(self) -> int:
        """Provides private default channel count value"""
        return self._default_channel_count

    @staticmethod
    def get_base_extensions() -> Set[str]:
        """ Provides extensions being used by class """
        return WAVEFILE_EXTENSIONS


class MP3FileType(AudioFileType):
    """Standard MP3 File Type Class"""

    def __init__(
        self,
        name: str = None,
        extension: Union[str, Set[str]] = None,
        bit_rate: Union[int, Set[int]] = None,
    ):
        super().__init__(
            name=name if name else "MP3 Audio file",
            short_name="mp3",
            extension=extension if extension else MP3_EXTENSIONS,
        )
        self.bit_rates = (
            {bit_rate}
            if bit_rate
            else STANDARD_BIT_RATE_PER_SECOND_RANGE
        )
        self._default_bit_rate = max(self.bit_rates)
        self.set_default_sample_rate(48000)
        self.set_default_extension("mp3")

    def set_default_bit_rate(self, bit_rate: int) -> None:
        """Sets the private default bit rate value"""
        if bit_rate not in self.bit_rates:
            self.bit_rates = self.bit_rates.union({bit_rate})
        self._default_bit_rate = bit_rate

    def get_default_bit_rate(self) -> int:
        """Provides private default bit rate value"""
        return self._default_bit_rate


class AudioFile:
    """Base Audio File class"""

    def __init__(
        self,
        file_path: str,
        file_type: AudioFileType,
        sample_rate=None,
    ) -> None:
        self.file_path = file_path
        self.file_type = file_type()
        self.sample_rate = (
            sample_rate
            if sample_rate
            else file_type().get_default_sample_rate()
        )
        self._filename, self._directory = o_path.split(file_path)
        self._extension = o_path.splitext(file_path)[1]
        if self._extension not in file_type().extensions:
            raise ValueError(
                f'File extension provided "{file_path=},{self._extension=}" \
                    not present in AudioFileType: {file_type=}'
            )
        self._file_exists = o_path.exists(file_path)
        self._directory_exists = o_path.isdir(o_path.split(file_path)[0])
        self._raw_data: Optional[bytes] = None

    def __eq__(self, other):
        if not isinstance(other, AudioFile):
            return NotImplemented
        return self.sample_rate == other.sample_rate

    def __ne__(self, other):
        if not isinstance(other, AudioFile):
            return NotImplemented
        return self.sample_rate != other.sample_rate

    def __str__(self):
        attributes = [
            f"  {k} = '{v}'\n"
            for k, v
            in self.__dict__.items() if k[0] != '_'
        ]
        return (
            f"{self.__class__.__name__}\n{''.join(attributes)}"
        )

    def __repr__(self):
        attributes = [
            f"{k}='{v}'"
            for k, v
            in self.__dict__.items()
            if k[0] != '_'
        ]
        private_attributes = [
            f"{k}='{v}'"
            for k, v
            in self.__dict__.items()
            if k[0] == '_'
        ]
        return (
            f"<{self.__class__.__name__} "
            f"{' '.join(attributes)} {' '.join(private_attributes)} >"
        )

    def get_file_extensions(self):
        """ Method to expose file_type extensions attribute """
        return self.file_type.get_extensions()

    def read_audio_file_metadata(self):
        """Method to observe the audio file metadata"""
        return True

    def resample_audio_file(self, new) -> bool:
        """Method to resample the audio file metadata"""
        print(new)
        return True

    def update_existance(self):
        """Validate whether or not the file exists"""
        self._file_exists = o_path.exists(self.file_path)
        self._directory_exists = o_path.isdir(self._directory)

    def does_file_exist(self) -> bool:
        """
        Return private value for if file exists.
        uses self.update_existance() and os.path.exists
        """
        return self._file_exists

    def does_directory_exist(self) -> bool:
        """
        Return private value for if directory exists.
        Uses self.update_existance() and os.path.isdir
        """
        return self._directory_exists

    def convert(
        self,
        candidate,
    ):
        """
        Converts file from an existing value to a target value
        Returns True if file was converted
        """
        if isinstance(candidate, AudioFile) and candidate != self:
            self.resample_audio_file(candidate)
            return True
        return False


class WaveFile(AudioFile):
    """Wave File class"""

    def __init__(
        self,
        file_path: str,
        file_type: AudioFileType = WaveFileType,
        channel_count: int = None,
        sample_rate: int = None,
        bit_depth: int = None,
    ) -> None:
        super().__init__(
            file_path=file_path,
            file_type=file_type,
            sample_rate=sample_rate,
        )
        self.bit_depth = (
            bit_depth
            if bit_depth
            else file_type().get_default_bit_depth()
        )
        self.channel_count = (
            channel_count
            if channel_count
            else file_type().get_default_channel_count()
        )
        self._metadata: self.WaveData = None

    def __eq__(self, other):
        self.read_audio_file_metadata()
        if not isinstance(other, AudioFile):
            return NotImplemented
        return (
            self.channel_count == other.channel_count
            and self.sample_rate == other.sample_rate
            and self.bit_depth == other.bit_depth
        )

    def __ne__(self, other):
        self.read_audio_file_metadata()
        if not isinstance(other, AudioFile):
            return NotImplemented
        return (
            self.channel_count != other.channel_count
            or self.sample_rate != other.sample_rate
            or self.bit_depth != other.bit_depth
        )

    @dataclass
    class WaveData:
        """Dataclass for Wave File Metadata"""

        number_of_channels: int
        bit_depth: int
        bit_width: int
        sample_rate: int
        comp: str
        compname: str

    def read_wave_file_metadata(self) -> None:
        """Overwrites instance values with current file metadata"""
        with wave.open(self.file_path, "rb") as wav_file:
            channels, width, rate, _, comp, compname = wav_file.getparams()
        self._metadata = self.WaveData(
            number_of_channels=channels,
            bit_depth=width * 8,
            bit_width=width,
            sample_rate=rate,
            comp=comp,
            compname=compname,
        )

    def get_exisiting_wave_file_metadata(self) -> WaveData:
        """Provides private metadata value"""
        if not self._metadata:
            self.read_wave_file_metadata()

    def update_instance_metadata(self) -> None:
        """Updates the instance values with actual values"""
        self.read_audio_file_metadata()
        self.bit_depth = self._metadata.bit_depth
        self.sample_rate = self._metadata.sample_rate
        self.channel_count = self._metadata.number_of_channels

    def read_audio_file_metadata(self):
        return self.read_wave_file_metadata()

    def resample_audio_file(self, new):
        # type: (WaveFile)->None
        self.update_instance_metadata()
        new_metadata = self.WaveData(
            number_of_channels=self._metadata.number_of_channels,
            bit_depth=new.bit_depth,
            bit_width=new.bit_depth // 8,
            sample_rate=new.sample_rate,
            comp=self._metadata.comp,
            compname=self._metadata.compname,
        )
        with wave.open(self.file_path, "rb") as wav_file:
            with wave.open(new.file_path, "wb") as new_audio_file:
                if isinstance(new_audio_file, wave.Wave_write):
                    new_audio_file.setparams(
                        (
                            new_metadata.number_of_channels,
                            new_metadata.bit_width,
                            new_metadata.sample_rate,
                            0,
                            new_metadata.comp,
                            new_metadata.compname,
                        )
                    )
                    data = wav_file.readframes(wav_file.getnframes())
                    new_audio_file.writeframes(data)

    @staticmethod
    def get_base_extensions() -> Set[str]:
        """ Provides extensions being used by class """
        return WAVEFILE_EXTENSIONS
