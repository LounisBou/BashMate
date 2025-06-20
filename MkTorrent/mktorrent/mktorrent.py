#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse

from .mediainfo import MediaInfo
from .contentanalyzer import ContentAnalyzer
from .contentgenerator import ContentGenerator

"""
MkTorrent - A tool to create torrent files, NFO files, and BBCode descriptions for media content.

This script analyzes media files in a directory, extracts metadata using mediainfo,
and generates appropriate torrent, NFO, and BBCode files.
"""

class MkTorrent:
    """
    Main class to create torrent, NFO, and BBCode files for media content.
    """

    def __init__(self, folder_path: str, tracker_url: str = "http://tracker.example.com:6969/announce"):
        """
        Initialize the MkTorrent object.
        
        :param folder_path: str - Path to the folder containing media content
        :param tracker_url: str - URL of the tracker (Default: "http://tracker.example.com:6969/announce")
        """
        self.folder_path = os.path.abspath(folder_path)
        self.tracker_url = tracker_url
        
        # Validate folder
        if not os.path.isdir(self.folder_path):
            raise ValueError(f"Error: {self.folder_path} is not a valid directory")
        
        # Initialize components
        self.analyzer = ContentAnalyzer(self.folder_path)
        first_video = self.analyzer.find_first_video_file()
        self.media_info = MediaInfo(first_video).metadata
        self.generator = ContentGenerator(self.media_info, self.analyzer)
        self.torrent_title = self.generator.generate_torrent_title()

    def create_torrent(self) -> bool:
        """
        Create the torrent file using mktorrent.
        
        :return: bool - True if successful, False otherwise
        """
        torrent_file = f"{self.torrent_title}.torrent"
        
        try:
            command = [
                'mktorrent',
                '-v',                     # Verbose mode
                '-l', '24',               # Piece size (24 = 16 MB)
                '-a', self.tracker_url,   # Tracker URL
                '-o', torrent_file,       # Torrent file name
                self.folder_path          # Source folder
            ]
            
            subprocess.run(command, check=True)
            print(f"Torrent file created successfully: {torrent_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating torrent: {e}")
            return False
        except FileNotFoundError:
            print("mktorrent command not found or not in PATH")
            return False

    def create_nfo(self) -> bool:
        """
        Create the NFO file.
        
        :return: bool - True if successful, False otherwise
        """
        nfo_file = f"{self.torrent_title}.nfo"
        
        try:
            nfo_content = self.generator.generate_nfo_content()
            with open(nfo_file, 'w', encoding='utf-8') as f:
                f.write(nfo_content)
            print(f"NFO file created: {nfo_file}")
            return True
        except Exception as e:
            print(f"Error creating NFO file: {e}")
            return False

    def create_bbcode(self) -> bool:
        """
        Create the BBCode description file.
        
        :return: bool - True if successful, False otherwise
        """
        bbcode_file = f"{self.torrent_title}.txt"
        
        try:
            bbcode_content = self.generator.generate_bbcode_content()
            with open(bbcode_file, 'w', encoding='utf-8') as f:
                f.write(bbcode_content)
            print(f"BBCode description created: {bbcode_file}")
            return True
        except Exception as e:
            print(f"Error creating BBCode file: {e}")
            return False

    def create_all(self) -> bool:
        """
        Create all files: torrent, NFO, and BBCode.
        
        :return: bool - True if all operations were successful, False otherwise
        """
        nfo_success = self.create_nfo()
        bbcode_success = self.create_bbcode()
        torrent_success = self.create_torrent()
        
        return nfo_success and bbcode_success and torrent_success


def main():
    """
    Main entry point for the script when run from command line.
    """
    parser = argparse.ArgumentParser(description='Create a torrent, NFO, and BBCode description from a folder.')
    parser.add_argument('folder', help='Path to the folder to process')
    parser.add_argument('--tracker', '-t', default='http://tracker.example.com:6969/announce', 
                        help='Tracker URL (default: http://tracker.example.com:6969/announce)')
    
    args = parser.parse_args()
    
    try:
        creator = MkTorrent(args.folder, args.tracker)
        success = creator.create_all()
        
        if success:
            print("All files created successfully!")
            return 0
        else:
            print("Some operations failed. Check the output above for details.")
            return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


