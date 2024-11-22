#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import re
from typing import List
from pathlib import Path

class NodeNameCleaner:

    """
    A class to clean name by removing unwanted characters and words.
    """

    CHARS_TO_CLEAN: List[str] = ["5.1", "4.0", ".", "-", "_", "[", "]", "{", "}", "~", "+", "(", ")", "!"]
    WORDS_TO_CLEAN = [
        "1080", "1080i", "1080p", "10bit", "10-bit", "1920x1080", "2160p", "2ch", "2vf", "480p", "720p", "7sins",
        "4k", "4klight", "6ch", "aac", "aaclc", "abcollection", "ac 3", "ac3", "acc", "acool",
        "amzn", "ark01", "av1", "avc", "bbc", "bbt", "bdrip", "benh4", "bit", "blank", "bluray", "bluray1080p",
        "brrip", "btt", "buret", "ccats", "ch", "chill", "chris44", "custom", "cut", "darkjuju", "dd", "ddp",
        "directors cut", "dl", "dolby vision", "dread team", "dts", "dvdrip", "dvd rip", "eac3", 
        "eaulive", "elcrackito", "en", "eng", "extended", "extreme", "fasandraeberne", "fervex", "final cut", "flaskepost",
        "fr", "fre", "french", "french(vff)", "frosties", "ftmvhd", "fw", "gbx", "ght", "ghz", 
        "gismo65", "gwen", "h264", "h265", "h4s5s", "hd", "hdl", "hdlight", "hdma", "hdr", "hdtv", 
        "he", "hevc", "hush", "integral", "integrale", "internal", "jiheff", "k7", "kaf", "kfl", 
        "kvinden", "lazarus", "lcds", "libertad", "luminus", "mhd", "mhdgz", "mkv", "mm91", "moe", 
        "mtl666", "multi", "multi3", "nf", "noex", "nobodyperfect", "non censurée", "none", "notag", "nyu", 
        "owii", "p4t4t3", "pop", "pophd", "Portos", "portos", "qtz", "remastered", "repack", "romkent", "se7en", 
        "serqph", "shc23", "slayer", "slay3r", "sn2p", "srt", "stereo", "tf", "title1", "tonyk", "tr", 
        "truefrench", "trunkdu92", "tvwh0res", "unrated", "uptopol", "utt", "version", "vf", "vf2", 
        "vff", "vfi", "vfq", "vlis", "vmpp", "vo", "vof", "vost", "vostfr", "vp9", "web", "web dl", "webdl", 
        "webrip", "x264", "x265", "xvid", "zeusfaber", "zone80", "zza"
    ]

    # Private methods

    @staticmethod
    def __clean_node_stem_chars(node_stem: str, replacement = ' ') -> str:
        """
        Cleans unwanted characters from the node stem.

        :param node_stem: Node name without the extension.
        :param replacement: Character to replace unwanted characters with. Default is a space.
        :return: The node stem with unwanted characters removed.
        """
        for char in NodeNameCleaner.CHARS_TO_CLEAN:
            node_stem = node_stem.replace(char, ' ')
        return node_stem

    @staticmethod
    def __clean_node_stem_words(node_stem: str, replacement = ' ') -> str:
        """
        Cleans unwanted words from the node stem.

        :param node_stem: Node name without the extension.
        :param replacement: Character to replace unwanted words with. Default is a space.
        :return: The node stem with unwanted words removed.
        """
        for word_to_clean in NodeNameCleaner.WORDS_TO_CLEAN:
            node_stem = re.sub(rf'\b{word_to_clean}\b', '', node_stem)
        return node_stem.strip()

    @staticmethod
    def __clean_node_stem(node_stem: str) -> str:
        """
        Cleans both unwanted characters and words from the node stem.

        :param node_stem: Node name without the extension.
        :return: The cleaned node stem.
        """
        # Convert to lowercase
        node_stem = node_stem.lower()
        # Remove elements in brackets
        node_stem = re.sub(r'\[.*?\]', '', node_stem, flags=re.IGNORECASE)
        # Remove elements in parentheses
        node_stem = re.sub(r'\(.*?\)', '', node_stem, flags=re.IGNORECASE)
        # Remove leading and trailing spaces
        node_stem = node_stem.strip()
        # Remove unwanted characters
        node_stem = NodeNameCleaner.__clean_node_stem_chars(node_stem)
        # Remove unwanted words
        node_stem = NodeNameCleaner.__clean_node_stem_words(node_stem)
        # Remove multiple spaces in a row
        node_stem = NodeNameCleaner.cleanup_extra_space(node_stem)
        # Remove leading and trailing spaces
        return node_stem.strip()
    
    # Public methods
    
    @staticmethod
    def cleanup_extra_space(node_name: str) -> str:
        """
        Cleans extra spaces from the node name.

        :param node_name: The name of the node.
        :return: The node name without extra spaces.
        """
        return re.sub(r'\s+', ' ', node_name)

    @staticmethod
    def get_cleaned_node_stem(path: Path) -> str:
        """
        Gets the cleaned node stem of a node.

        :param path: The full path of the node.
        :return: The cleaned node stem.
        """
        # Check if the path is a directory
        if path.is_dir():
            return NodeNameCleaner.__clean_node_stem(path.name)
        else:
            return NodeNameCleaner.__clean_node_stem(path.stem)
    
    @staticmethod
    def get_cleaned_node_name(path: Path) -> str:
        """
        Gets the cleaned node name of a node.

        :param path: The full path of the node.
        :return: The cleaned node name.
        """
        # Check if the path is a directory
        if path.is_dir():
            return NodeNameCleaner.__clean_node_stem(path.name)
        else:
            return NodeNameCleaner.__clean_node_stem(path.stem) + path.suffix
    
    @staticmethod
    def get_year_from_node_name(node_name: str) -> int|None:
        """
        Gets the year from the node name if it exists. Otherwise, returns None.
        Allowed Paterns: 19xx or 20xx
        :param node_name: The name of the node.
        :return: The year from the node name, if it exists. Otherwise, None.
        """
        # Get the year from the node name
        year = re.search(r'\b(19|20)\d{2}\b', node_name, flags=re.IGNORECASE)
        # Return the year as an integer if it exists
        return int(year.group()) if year else None
    
    @staticmethod
    def get_season_and_episode_from_node_name(node_name: str) -> tuple[int|None, int|None]:
        """
        Gets the season and episode from the node name if it exists. Otherwise, returns None.
        Allowed paterns: sxxexx, sxxexxx, saison xx episode xx, saison xx episode xxx
        :param node_name: The name of the node.
        :return: The season from the node name.
        """
        # Get the season and episode from the node name
        pattern = r"(?i)s(?:aison|eason)?\s*(\d{1,2})e(?:pisode)?\s*(\d{1,2})|s(?:aison|eason)?\s*(\d{1,2})|e(?:pisode)?\s*(\d{1,2})"
        
        # Match the pattern
        match = re.findall(pattern, node_name)

        # Initialize season and episode
        season = None
        episode = None

        # Loop through the groups in the match
        for groups in match:
            # Handle groups for both season and episode
            if groups[0] and groups[1]:  # Case: s01e04
                season = int(groups[0])
                episode = int(groups[1])
                break  # Stop after finding both season and episode
            elif groups[0]:  # Case: saison 1 or s01
                season = int(groups[0])
            elif groups[1]:  # Case: e04
                episode = int(groups[1])
                
        return season, episode

    @staticmethod
    def get_name_without_year(node_name: str) -> str:
        """
        Gets the node name without the year.
        :param node_name: The name of the node.
        :return: The node name without the year.
        """
        # Pattern to match year information
        pattern_year = r"\b(19|20)\d{2}\b"
        
        # Remove matches from the node name
        cleaned_name = re.sub(pattern_year, "", node_name, flags=re.IGNORECASE).strip()
        
        # Clean up extra spaces
        cleaned_name = NodeNameCleaner.cleanup_extra_space(cleaned_name)
        
        return cleaned_name
    
    @staticmethod
    def get_name_without_season_and_episode(node_name: str) -> str:
        """
        Gets the node name without the season and/or episode.
        :param node_name: The name of the node.
        :return: The node name without the season and episode.
        """
        # Pattern to match season and episode information
        pattern_season = r"(?i)(?:\bs(?:aison|eason)?\s*\d{1,2})"
        # Pattern to match episode information
        pattern_episode = r"(?i)(?:\be(?:pisode)?\s*\d{1,2})"
        
        # Remove matches from the node name
        cleaned_name = re.sub(pattern_season, "", node_name, flags=re.IGNORECASE).strip()
        cleaned_name = re.sub(pattern_episode, "", cleaned_name, flags=re.IGNORECASE).strip()
        
        # Clean up extra spaces
        cleaned_name = NodeNameCleaner.cleanup_extra_space(cleaned_name)
        
        return cleaned_name