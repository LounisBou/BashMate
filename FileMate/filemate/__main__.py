#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from pathlib import Path
from filemate import Directory

def main():
    """
    The main function of the program.
    """
    # Path 
    path = Path("/Volumes/IznoServer SSD/torrents")
    # Directory
    directory = Directory(path)
    # Print the directory
    print(directory)
    
    
# Check if the script is being run directly
if __name__ == "__main__":
    main()