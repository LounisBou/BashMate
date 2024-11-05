#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from enum import Enum
from pathlib import Path
import re
from .file_type_extensions import FileTypeExtensions

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
        for file_type in FileTypeExtensions.types():
            extensions = FileTypeExtensions[file_type].value
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
        media_extensions = FileTypeExtensions[FileType.VIDEO] + FileTypeExtensions[FileType.AUDIO]
        extension = filepath.suffix[1:].lower()
        return extension in media_extensions
