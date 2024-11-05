#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from enum import Enum
from pathlib import Path
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