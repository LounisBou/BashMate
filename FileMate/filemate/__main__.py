#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from .file_system_node_factory import FileSystemNodeFactory
from .file_sorter import FileSorter

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
    parser.add_argument('--verbose', action='store_true', required=False, help='Verbose output')
    parser.add_argument('--dry-run', action='store_true', required=False, help='Dry run')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Node path
    node_path = args.path
    # Path 
    path = Path(node_path)
    # Node
    node = FileSystemNodeFactory(path)
    # Sort nodes
    file_sorter = FileSorter(node, verbose=args.verbose, dry_run=args.dry_run)
    file_sorter.process()
    
    
# Check if the script is being run directly
if __name__ == "__main__":
    main()