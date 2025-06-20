#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
from datetime import datetime
from typing import Tuple, Set, Any

class ContentAnalyzer:
    """
    Class to analyze content directories and extract metadata about the content.
    """

    def __init__(self, folder_path: str):
        """
        Initialize the ContentAnalyzer with a folder path.
        
        :param folder_path: str - Path to the folder containing media content
        """
        self.folder_path = folder_path
        self.content_type = self._detect_content_type()
        self.title, self.year = self._extract_title_year()
        
        if self.content_type == "serie":
            self.episode_count = self._count_episodes()
            self.season_count = self._count_seasons()
            self.year_range = self._determine_year_range()
        else:
            self.episode_count = 1
            self.season_count = 1
            self.year_range = self.year

    def _detect_content_type(self) -> str:
        """
        Detect if the content is a movie or a TV series based on folder structure and filenames.
        
        :return: str - "serie" or "film"
        """
        folder_name = os.path.basename(os.path.normpath(self.folder_path))
        
        # Regex patterns to detect series (seasons, episodes)
        series_patterns = [
            r'[sS]\d+[eE]\d+',  # S01E01
            r'[sS]aison\s*\d+',  # Saison 1
            r'[sS]eason\s*\d+',  # Season 1
            r'saisons?\s*\d+',   # saison 1
            r'seasons?\s*\d+'    # season 1
        ]
        
        # Check folder name
        for pattern in series_patterns:
            if re.search(pattern, folder_name, re.IGNORECASE):
                return "serie"
        
        # Check subfolders
        for item in os.listdir(self.folder_path):
            full_path = os.path.join(self.folder_path, item)
            if os.path.isdir(full_path):
                for pattern in series_patterns:
                    if re.search(pattern, item, re.IGNORECASE):
                        return "serie"
        
        # Check files
        video_extensions = ['.mkv', '.mp4', '.avi']
        episode_count = 0
        
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    episode_count += 1
                    for pattern in series_patterns:
                        if re.search(pattern, file, re.IGNORECASE):
                            return "serie"
        
        # If multiple video files, probably a series
        if episode_count > 1:
            return "serie"
        
        # Default to movie
        return "film"

    def _extract_title_year(self) -> Tuple[str, str]:
        """
        Extract the title and year from the folder name.
        
        :return: Tuple[str, str] - (title, year)
        """
        folder_name = os.path.basename(os.path.normpath(self.folder_path))
        
        # Regex to extract title and year
        match = re.search(r'(.+?)\s*\((\d{4})(?:-\d{4})?\)', folder_name)
        
        if match:
            title = match.group(1).strip()
            year = match.group(2)
            return title, year
        
        # Try other formats if no year in parentheses
        match = re.search(r'(.+?)\s+(\d{4})(?:\s|$)', folder_name)
        if match:
            title = match.group(1).strip()
            year = match.group(2)
            return title, year
        
        # If no format matches, return folder name and empty year
        return folder_name, ""

    def _count_episodes(self) -> int:
        """
        Count the number of episodes (video files) in the folder.
        
        :return: int - Number of episodes
        """
        video_extensions = ['.mkv', '.mp4', '.avi']
        episode_count = 0
        
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    episode_count += 1
        
        return episode_count

    def _count_seasons(self) -> int:
        """
        Count the number of seasons in a series folder.
        
        :return: int - Number of seasons
        """
        season_patterns = [
            r'[sS]aison\s*\d+',  # Saison 1
            r'[sS]eason\s*\d+',  # Season 1
            r'saisons?\s*\d+',   # saison 1
            r'seasons?\s*\d+'    # season 1
        ]
        
        season_count = 0
        season_folders: Set[str] = set()
        
        # Look for season folders
        for item in os.listdir(self.folder_path):
            full_path = os.path.join(self.folder_path, item)
            if os.path.isdir(full_path):
                for pattern in season_patterns:
                    if re.search(pattern, item, re.IGNORECASE):
                        season_folders.add(item)
                        season_count += 1
                        break
        
        # If no season folders, check video files
        if season_count == 0:
            season_numbers: Set[int] = set()
            video_extensions = ['.mkv', '.mp4', '.avi']
            
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in video_extensions):
                        # Look for S01E01 or similar
                        match = re.search(r'[sS](\d+)[eE]', file)
                        if match:
                            season_numbers.add(int(match.group(1)))
            
            season_count = len(season_numbers)
        
        return max(1, season_count)  # At least 1 season

    def _determine_year_range(self) -> str:
        """
        Determine the year range for a series.
        
        :return: str - Year range (e.g., "1997-2007")
        """
        if not self.year:
            return "Unknown"
            
        try:
            start_year = int(self.year)
            # By default, assume series lasted ~2 years per season
            end_year = min(start_year + max(1, self.season_count // 2), datetime.now().year)
            return f"{start_year}-{end_year}"
        except ValueError:
            return self.year

    def find_first_video_file(self) -> str:
        """
        Find the first video file in the folder (recursively).
        
        :return: str - Path to the first video file
        """
        video_extensions = ['.mkv', '.mp4', '.avi']
        
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    return os.path.join(root, file)
        
        print("No video files found in the folder.")
        sys.exit(1)
