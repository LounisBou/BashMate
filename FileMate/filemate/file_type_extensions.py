#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from enum import Enum

class FileTypeExtensions(Enum):

    """
    Enum class for file types.
    """

    # Media extensions
    VIDEO = [
        "avi", "mkv", "mp4", "mpg", "mpeg", "mov", "wmv", "flv", "webm", "m4v",
        "3gp", "3g2", "asf", "rm", "swf", "vob", "ts", "m2ts", "mts", "m2t",
        "m4p", "m4b", "m4r", "m4a", "f4v", "f4a", "f4b", "f4p", "f4r", "ogg",
        "ogv", "oga", "ogx", "ogm", "spx", "opus", "flac", "wav", "mp3", "wma",
        "aac", "ac3", "dts", "pcm", "mka", "mks", "weba", "ra", "rmvb"
    ]
    AUDIO = [
        "mp3", "wav", "flac", "ogg", "m4a", "wma", "aac", "ac3", "dts", "pcm",
        "mka", "mks", "weba", "ra", "rmvb"
    ]
    ARCHIVE = ["zip", "rar", "7z", "tar", "gz", "bz2", "xz"]
    IMAGE = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"]
    SUBTITLE = ["srt", "sub", "sbv", "vtt"]
    EBOOK = ["pdf", "epub", "mobi", "azw", "azw3", "djvu", "cbz", "cbr", "fb2", "lit"]
    DOCUMENT = ["doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "txt"]
    APP = ["exe", "msi", "dmg", "pkg", "deb", "rpm", "sh", "bat", "cmd"]
    ANDROID = ["apk"]
    ISO = ["iso", "img", "bin", "cue", "nrg", "mdf", "mds", "ccd", "cif", "c2d"]
    SCRIPT = [
        "py", "sh", "bat", "cmd", "ps1", "vbs", "js", "php", "pl", "rb", "java", "cpp", "cs",
        "html", "css", "xml", "json", "yaml", "yml", "toml", "ini", "cfg", "conf", "log", "md", "rst"
    ]
    OTHER = ["nfo", "url", "torrent", "csv"]
    
    @classmethod
    def types(cls) -> dict:
        """
        Allow to get all the enum members to iterate.
        @return: A dict with all the enum members.
        """
        return cls.__members__
    
    @classmethod
    def keys(cls):
        """"
        Returns the keys of the enum.
        """
        return cls.__members__.keys()
    
    @classmethod
    def get_file_type(cls, extension):
        """
        Returns the FileTypeExtensions member associated with the given extension.
        """
        for file_type in cls:
            if extension.lower() in file_type.value:
                return file_type
        return None
    