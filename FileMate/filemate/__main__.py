#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from .file_system_node_factory import FileSystemNodeFactory

def main():
    """
    Entry point for the FileMate application.
    """
    
    # Create the parser
    parser = argparse.ArgumentParser(description='FileMate - A file management tool.')
    parser.add_argument('path', type=Path, help='Path to the fileSystem node to process')
    parser.add_argument('--clean', action='store_true', required=False, help='Clean file names')
    parser.add_argument('--sort', action='store_true', required=False, help='Sort files into subdirectories')
    parser.add_argument('--delete-empty', action='store_true', required=False, help='Delete empty subdirectories')
    parser.add_argument('--delete-duplicates', action='store_true', required=False, help='Delete duplicate files')
    parser.add_argument('--delete-small', action='store_true', required=False, help='Delete small files')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Node path
    node_path = args.path
    # Path 
    path = Path(node_path)
    # Node
    node = FileSystemNodeFactory.create_node(path)
    # Check if the node is a directory
    if node.is_dir():
        # Iterate over sub nodes
        for sub_node in node:
            print(sub_node)
            print('--------------------------------------------------')
    else:
        print(node)
    
    
# Check if the script is being run directly
if __name__ == "__main__":
    main()