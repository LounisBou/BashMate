#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from .directory import Directory


def main():
    """
    Entry point for the FileMate application.
    """
    
    # Create the parser
    parser = argparse.ArgumentParser(description='FileMate - A file management tool.')
    parser.add_argument('directory', type=Path, help='Path to the directory to process')
    parser.add_argument('--clean', action='store_true', required=False, help='Clean file names')
    parser.add_argument('--sort', action='store_true', required=False, help='Sort files into subdirectories')
    parser.add_argument('--delete-empty', action='store_true', required=False, help='Delete empty subdirectories')
    parser.add_argument('--delete-duplicates', action='store_true', required=False, help='Delete duplicate files')
    parser.add_argument('--delete-small', action='store_true', required=False, help='Delete small files')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Directory path
    directory_path = args.directory
    # Path 
    path = Path(directory_path)
    # Directory
    directory = Directory(path)
    # Print the directory
    print(directory)
    
    
# Check if the script is being run directly
if __name__ == "__main__":
    main()