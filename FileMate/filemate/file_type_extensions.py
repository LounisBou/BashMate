#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from enum import Enum as enum
from pathlib import Path
from filemate import FileType

class FileTypeExtensions(enum):

    """
    Enum class for file types.
    """

    # Media extensions
    FileType.VIDEO = [
        "avi", "mkv", "mp4", "mpg", "mpeg", "mov", "wmv", "flv", "webm", "m4v",
        "3gp", "3g2", "asf", "rm", "swf", "vob", "ts", "m2ts", "mts", "m2t",
        "m4p", "m4b", "m4r", "m4a", "f4v", "f4a", "f4b", "f4p", "f4r", "ogg",
        "ogv", "oga", "ogx", "ogm", "spx", "opus", "flac", "wav", "mp3", "wma",
        "aac", "ac3", "dts", "pcm", "mka", "mks", "weba", "ra", "rmvb"
    ]
    FileType.TVSHOW = FileType.VIDEO
    FileType.MOVIE = FileType.VIDEO
    FileType.AUDIO = [
        "mp3", "wav", "flac", "ogg", "m4a", "wma", "aac", "ac3", "dts", "pcm",
        "mka", "mks", "weba", "ra", "rmvb"
    ]
    FileType.ARCHIVE = ["zip", "rar", "7z", "tar", "gz", "bz2", "xz"]
    FileType.IMAGE = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"]
    FileType.SUBTITLE = ["srt", "sub", "sbv", "vtt"]
    FileType.EBOOK = ["pdf", "epub", "mobi", "azw", "azw3", "djvu", "cbz", "cbr", "fb2", "lit"]
    FileType.DOCUMENT = ["doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "txt"]
    FileType.APP = ["exe", "msi", "dmg", "pkg", "deb", "rpm", "sh", "bat", "cmd"]
    FileType.ANDROID = ["apk"]
    FileType.ISO = ["iso", "img", "bin", "cue", "nrg", "mdf", "mds", "ccd", "cif", "c2d"]
    FileType.SCRIPT = [
        "py", "sh", "bat", "cmd", "ps1", "vbs", "js", "php", "pl", "rb", "java", "cpp", "cs",
        "html", "css", "xml", "json", "yaml", "yml", "toml", "ini", "cfg", "conf", "log", "md", "rst"
    ]
    
    @classmethod
    def types(cls) -> list:
        """
        Allow to get all the enum members to iterate.
        @return: A list of all enum members.
        """
        return list(cls)
    