#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from filemate import Directory
from pathlib import Path

def main():
    """
    Entry point for running FileMate directly via main.py.
    """
    directory_path = Path('/Volumes/IznoServer SSD/torrents')  # You can hardcode for testing or parse arguments
    directory = Directory(directory_path)

    # Perform actions
    # Example: Clean and sort
    # Implement logic or call functions from your package

if __name__ == '__main__':
    main()