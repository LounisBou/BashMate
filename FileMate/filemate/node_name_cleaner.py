#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import os
import re
from typing import List
from pathlib import Path
from dotenv import load_dotenv

@dataclass
class NodeNameCleaner:
    
    """
    A class to clean name by removing unwanted characters and words.
    """

    cleaning_chars_path: str|None = field(init=False, default=None, metadata="Path to the file containing the cleaning characters.")
    cleaning_words_path: str|None = field(init=False, default=None, metadata="Path to the file containing the cleaning words.")
    cleaning_chars: List[str] = field(init=False, default_factory=List[str], metadata="List of characters to clean.")
    cleaning_words: List[str] = field(init=False, default_factory=List[str], metadata="List of words to clean.")
    
    def __init__(self):
        """
        Initializes the NodeNameCleaner class.
        """
        load_dotenv()
        # Current directory of the script
        main_script_dir = Path(__file__).parent.resolve().parent
        self.cleaning_chars_path = main_script_dir / os.getenv("CLEAN_CHARACTERS_FILE")
        self.cleaning_words_path = main_script_dir / os.getenv("CLEAN_WORDS_FILE")
        self.__load_cleaning_chars()
        self.__load_cleaning_words()
        
    def __load_cleaning_chars(self):
        """
        Loads the cleaning characters from the .env file.
        """
        with open(self.cleaning_chars_path, "r", encoding="utf-8") as file:
            self.cleaning_chars = file.read().splitlines()
              
    def __load_cleaning_words(self):
        """
        Loads the cleaning words from the .env file.
        """
        with open(self.cleaning_words_path, "r", encoding="utf-8") as file:
            self.cleaning_words = file.read().splitlines()
        
    # Private methods

    
    def __clean_node_stem_chars(self, node_stem: str, replacement = ' ') -> str:
        """
        Cleans unwanted characters from the node stem.
        :param node_stem: Node name without the extension.
        :param replacement: Character to replace unwanted characters with. Default is a space.
        :return: The node stem with unwanted characters removed.
        """
        for char_to_clean in self.cleaning_chars:
            node_stem = node_stem.replace(char_to_clean, replacement)
        return node_stem

    def __clean_node_stem_words(self, node_stem: str, replacement = '') -> str:
        """
        Cleans unwanted words from the node stem.
        :param node_stem: Node name without the extension.
        :param replacement: Character to replace unwanted words with. Default is a space.
        :return: The node stem with unwanted words removed.
        """
        for word_to_clean in self.cleaning_words:
            node_stem = re.sub(rf'\b{word_to_clean}\b', replacement, node_stem)
        return node_stem.strip()

    def __clean_node_stem(self, node_stem: str) -> str:
        """
        Cleans both unwanted characters and words from the node stem.
        :param node_stem: Node name without the extension.
        :return: The cleaned node stem.
        """
        # Convert to lowercase
        node_stem = node_stem.lower()

        # Remove leading and trailing spaces
        node_stem = node_stem.strip()
        # Remove unwanted characters
        node_stem = self.__clean_node_stem_chars(node_stem)
        # Remove unwanted words
        node_stem = self.__clean_node_stem_words(node_stem)
        # Remove multiple spaces in a row
        node_stem = self.cleanup_extra_space(node_stem)
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

    def get_cleaned_node_stem(self, path: Path) -> str:
        """
        Gets the cleaned node stem of a node.
        :param path: The full path of the node.
        :return: The cleaned node stem.
        """
        # Check if the path is a directory
        if path.is_dir():
            return self.__clean_node_stem(path.name)
        else:
            return self.__clean_node_stem(path.stem)
    
    def get_cleaned_node_name(self, path: Path) -> str:
        """
        Gets the cleaned node name of a node.
        :param path: The full path of the node.
        :return: The cleaned node name.
        """
        # Check if the path is a directory
        if path.is_dir():
            return self.__clean_node_stem(path.name)
        else:
            return self.__clean_node_stem(path.stem) + path.suffix
    
    def get_year_from_node_name(self, node_name: str) -> int|None:
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
    
    def get_season_and_episode_from_node_name(self, node_name: str) -> tuple[int|None, int|None]:
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
                
            # Handle groups for both season and episode (second case)
            elif groups[2] and groups[3]:
                season = int(groups[2])
                episode = int(groups[3])
                break
            elif groups[2]:
                season = int(groups[2])
            elif groups[3]:
                episode = int(groups[3])
                
        return season, episode

    def get_name_without_year(self, node_name: str) -> str:
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
        cleaned_name = self.cleanup_extra_space(cleaned_name)
        
        return cleaned_name
    
    def get_name_without_season_and_episode(self, node_name: str) -> str:
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
        cleaned_name = self.cleanup_extra_space(cleaned_name)
        
        return cleaned_name