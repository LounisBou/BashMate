#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import re
from typing import List
from pathlib import Path

class FileNameCleaner:

    """
    A class to clean filenames by removing unwanted characters and words.
    """

    CHARS_TO_CLEAN: List[str] = ["5.1", "4.0", ".", "-", "_", "[", "]", "{", "}", "~", "+", "(", ")", "!"]
    WORDS_TO_CLEAN = [
        "1080", "1080i", "1080p", "10bit", "1920x1080", "2160p", "2vf", "480p", "720p", "7sins",
        "4k", "4klight", "6ch", "aac", "aaclc", "abcollection", "ac 3", "ac3", "acc", "acool",
        "amzn", "ark01", "av1", "avc", "bbc", "bbt", "bdrip", "benh4", "bit", "bluray", "bluray1080p",
        "brrip", "btt", "buret", "ccats", "ch", "chris44", "custom", "darkjuju", "dd", "ddp",
        "directors cut", "dl", "dolby vision", "dread team", "dts", "dvdrip", "dvd rip", "eac3", 
        "eaulive", "en", "eng", "extended", "extreme", "fasandraeberne", "final cut", "flaskepost",
        "fr", "fre", "french", "french(vff)", "frosties", "ftmvhd", "fw", "gbx", "ght", "ghz", 
        "gismo65", "gwen", "h264", "h265", "h4s5s", "hd", "hdl", "hdlight", "hdma", "hdr", "hdtv", 
        "he", "hevc", "hush", "integral", "integrale", "internal", "jiheff", "k7", "kaf", "kfl", 
        "kvinden", "lazarus", "lcds", "libertad", "luminus", "mhd", "mhdgz", "mkv", "mm91", "moe", 
        "mtl666", "multi", "multi3", "nf", "noex", "nobodyperfect", "non censurée", "notag", "nyu", 
        "owii", "p4t4t3", "pop", "pophd", "Portos", "portos", "qtz", "remastered", "romkent", "se7en", 
        "serqph", "shc23", "slayer", "slay3r", "srt", "stereo", "tf", "title1", "tonyk", "tr", 
        "truefrench", "trunkdu92", "tvwh0res", "unrated", "uptopol", "utt", "version", "vf", "vf2", 
        "vff", "vfi", "vfq", "vlis", "vmpp", "vo", "vof", "vost", "vostfr", "web", "web dl", "webdl", 
        "webrip", "x264", "x265", "xvid", "zeusfaber", "zone80", "zza"
    ]

    # Private methods

    @staticmethod
    def __clean_file_stem_chars(file_stem: str, replacement = ' ') -> str:
        """
        Cleans unwanted characters from the file stem.

        :param file_stem: Filename without the extension.
        :param replacement: Character to replace unwanted characters with. Default is a space.
        :return: The file stem with unwanted characters removed.
        """
        for char in FileNameCleaner.CHARS_TO_CLEAN:
            file_stem = file_stem.replace(char, ' ')
        return file_stem

    @staticmethod
    def __clean_file_stem_words(file_stem: str, replacement = ' ') -> str:
        """
        Cleans unwanted words from the file stem.

        :param file_stem: Filename without the extension.
        :param replacement: Character to replace unwanted words with. Default is a space.
        :return: The file stem with unwanted words removed.
        """
        for word in FileNameCleaner.WORDS_TO_CLEAN:
            file_stem = file_stem.replace(f" {word} ", ' ')
        return file_stem.strip()

    @staticmethod
    def __clean_file_stem(file_stem: str) -> str:
        """
        Cleans both unwanted characters and words from the file stem.

        :param file_stem: Filename without the extension.
        :return: The cleaned file stem.
        """
        file_stem = file_stem.lower()
        file_stem = FileNameCleaner.__clean_file_stem_chars(file_stem)
        file_stem = FileNameCleaner.__clean_file_stem_words(file_stem)
        # Remove multiple spaces in a row
        file_stem = re.sub(r'\s+', ' ', file_stem)
        # Remove leading and trailing spaces
        return file_stem.strip()
    
    # Public methods

    @staticmethod
    def get_cleaned_file_stem(filepath: Path) -> str:
        """
        Gets the cleaned file stem of a file.

        :param filepath: The full path of the file.
        :return: The cleaned file stem.
        """
        return FileNameCleaner.__clean_file_stem(filepath.stem)
    
    @staticmethod
    def get_cleaned_file_name(filepath: Path) -> str:
        """
        Gets the cleaned file name of a file.

        :param filepath: The full path of the file.
        :return: The cleaned file name.
        """
        return FileNameCleaner.__clean_file_stem(filepath.stem) + filepath.suffix

