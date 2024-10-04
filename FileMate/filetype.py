from enum import Enum
from pathlib import Path
import re

class FileType(Enum):
    """
    Enum class for file types.
    """
    VIDEO = "video"
    MOVIE = "movie"
    TVSHOW = "tvshow"
    EBOOK = "ebook"
    AUDIO = "audio"
    APP = "app"
    ANDROID = "android"
    ARCHIVE = "archive"
    IMAGE = "image"
    SUBTITLE = "subtitle"
    DOCUMENT = "document"
    ISO = "iso"
    SCRIPT = "script"
    OTHER = "other"

    # Class-level dictionary mapping FileType to extensions
    EXTENSIONS = {
        VIDEO: [
            "avi", "mkv", "mp4", "mpg", "mpeg", "mov", "wmv", "flv", "webm", "m4v",
            "3gp", "3g2", "asf", "rm", "swf", "vob", "ts", "m2ts", "mts", "m2t",
            "m4p", "m4b", "m4r", "m4a", "f4v", "f4a", "f4b", "f4p", "f4r", "ogg",
            "ogv", "oga", "ogx", "ogm", "spx", "opus", "weba", "ra", "rmvb"
        ],
        MOVIE: [
            # Assuming movies have the same extensions as VIDEO
            "avi", "mkv", "mp4", "mpg", "mpeg", "mov", "wmv", "flv", "webm", "m4v",
            # ... (same as VIDEO)
        ],
        TVSHOW: [
            # Assuming TV shows have the same extensions as VIDEO
            "avi", "mkv", "mp4", "mpg", "mpeg", "mov", "wmv", "flv", "webm", "m4v",
            # ... (same as VIDEO)
        ],
        AUDIO: [
            "mp3", "wav", "flac", "ogg", "m4a", "wma", "aac", "ac3", "dts", "pcm",
            "mka", "weba", "ra", "rmvb"
        ],
        ARCHIVE: ["zip", "rar", "7z", "tar", "gz", "bz2", "xz"],
        IMAGE: ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
        SUBTITLE: ["srt", "sub", "sbv", "vtt"],
        EBOOK: ["pdf", "epub", "mobi", "azw", "azw3", "djvu", "cbz", "cbr", "fb2", "lit"],
        DOCUMENT: ["doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "txt"],
        APP: ["exe", "msi", "dmg", "pkg", "deb", "rpm"],
        ANDROID: ["apk"],
        ISO: ["iso", "img", "bin", "cue", "nrg", "mdf", "mds", "ccd", "cif", "c2d"],
        SCRIPT: [
            "py", "sh", "bat", "cmd", "ps1", "vbs", "js", "php", "pl", "rb", "java",
            "cpp", "cs", "html", "css", "xml", "json", "yaml", "yml", "toml", "ini",
            "cfg", "conf", "log", "md", "rst"
        ],
    }

    @classmethod
    def get(cls, filepath: Path) -> 'FileType':
        """
        Gets the type of a file based on its extension.
        :param filepath: Path of the file.
        :return: The type of the file.
        """
        extension = filepath.suffix[1:].lower()  # Remove leading dot and convert to lowercase
        filename = filepath.stem.lower()

        # Check for TV Show pattern
        if re.search(r"s\d{1,2}e\d{1,2}", filename):
            return cls.TVSHOW

        # Iterate over the EXTENSIONS mapping
        for file_type, extensions in cls.EXTENSIONS.items():
            if extension in extensions:
                return file_type

        # If no match found, return OTHER
        return cls.OTHER

    @staticmethod
    def is_media(filepath: Path) -> bool:
        """
        Checks if a file is a media file based on its extension.
        :param filepath: Path of the file.
        :return: True if the file is a media file, False otherwise.
        """
        media_extensions = FileType.EXTENSIONS[FileType.VIDEO] + FileType.EXTENSIONS[FileType.AUDIO]
        extension = filepath.suffix[1:].lower()
        return extension in media_extensions
