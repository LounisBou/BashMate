#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from .file_system_node_factory import FileSystemNodeFactory
from .file_system_node_tree import FileSystemNodeTree
from .file_sorter import FileSorter

def main():
    """
    Entry point for the FileMate application.
    """
    
    # Create the parser
    parser = argparse.ArgumentParser(description='FileMate - A file management tool.')
    parser.add_argument('path', type=Path, help='Path to the fileSystem node to process')
    parser.add_argument('--sort', action='store_true', required=False, help='Sort the directory')
    parser.add_argument('--tree', action='store_true', required=False, help='Print the tree of the directory')
    parser.add_argument('--clean', action='store_true', required=False, help='Delete remaining elements of a sorted directory')
    parser.add_argument('--verbose', action='store_true', required=False, help='Verbose output')
    parser.add_argument('--dry-run', action='store_true', required=False, help='Dry run')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Node path
    node_path = args.path
    # Path 
    path = Path(node_path)
    # Node
    node = FileSystemNodeFactory(path)
    # Check if tree is requested
    if args.tree:
        # Check if the node tree saved file exists
        if FileSystemNodeTree.check_saved_tree(node.name):
            # Load the tree
            file_system_node_tree = FileSystemNodeTree.restore(node.name)
            # Print the tree
            file_system_node_tree.show()
        else:
            # Create the tree
            file_system_node_tree = FileSystemNodeTree(node, verbose=args.verbose)
            # Save the tree
            file_system_node_tree.save()
        # Print the tree
        file_system_node_tree.show()
    # Check if sort is requested
    if args.sort:
        # Sort nodes
        file_sorter = FileSorter(node, verbose=args.verbose, dry_run=args.dry_run)
        file_sorter.process(delete_remaining_element=args.clean)

        
    
# Check if the script is being run directly
if __name__ == "__main__":
    main()