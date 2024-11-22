#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import argparse
import asyncio
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from .file_system_node_factory import FileSystemNodeFactory
from .file_system_node_tree import FileSystemNodeTree
from .file_sorter import FileSorter


def get_logger(verbose: bool = False, console: bool = False, file: bool = False) -> None:
    """
    Create a logger.
    """
    # Determine logging level based on verbosity
    logging_level = logging.INFO if verbose else logging.DEBUG

    # Initialize the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging_level)

    # Disable propagation to avoid duplicate logs
    logger.propagate = False

    # Check if handlers are already added
    if not logger.hasHandlers():
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add console handler
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging_level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # Add file handler
        if file:
            try:
                file_handler = logging.FileHandler('filemate.log')
                file_handler.setLevel(logging_level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"Failed to create file handler: {e}")
    
    # Return the logger
    return logger

async def main(console: bool = False) -> None:
    """
    Entry point for the FileMate application.
    """
    
    # Create the parser
    parser = argparse.ArgumentParser(description='FileMate - A file management tool.')
    parser.add_argument('path', type=Path, help='Path to the fileSystem node to process')
    parser.add_argument('--sort', action='store_true', required=False, help='Sort the directory')
    parser.add_argument('--tree', action='store_true', required=False, help='Build the tree of the directory')
    parser.add_argument('--show-tree', action='store_true', required=False, help='Show the tree of the directory')
    parser.add_argument('--asynchronous', action='store_true', required=False, help='Build the tree of the directory asynchronously')
    parser.add_argument('--clean', action='store_true', required=False, help='Delete remaining elements of a sorted directory')
    parser.add_argument('--verbose', action='store_true', required=False, help='Verbose output')
    parser.add_argument('--dry-run', action='store_true', required=False, help='Dry run')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Get the logger
    logger = get_logger(verbose=args.verbose, console=True)
    
    # Max threads for the ThreadPoolExecutor
    max_threads = 6
    
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
        else:
            # If async is requested
            if args.asynchronous:
                # Create a ThreadPoolExecutor for multithreading
                with ThreadPoolExecutor(max_workers=max_threads) as executor:
                    # Set the default executor for asyncio
                    loop = asyncio.get_running_loop()
                    loop.set_default_executor(executor)
                    # Create the tree
                    file_system_node_tree = FileSystemNodeTree(
                        node, 
                        verbose=args.verbose, 
                        logger=logger
                    )
                    # Build the tree
                    await file_system_node_tree.async_build()
                    # Save the tree
                    file_system_node_tree.save()
            else:
                # Create the tree
                file_system_node_tree = FileSystemNodeTree(
                    node, 
                    verbose=args.verbose, 
                    logger=logger
                )
                # Build the tree
                file_system_node_tree.build()
                # Save the tree
                file_system_node_tree.save()
        # Print the node tree
        if args.show_tree:
            file_system_node_tree.show()
        
    # Check if sort is requested
    if args.sort:
        # Sort nodes
        file_sorter = FileSorter(
            node, 
            verbose=args.verbose, 
            dry_run=args.dry_run, 
            logger=logger,
        )
        file_sorter.process(delete_remaining_element=args.clean)      

  
# Check if the script is being run directly
if __name__ == "__main__":
    # Run the main function
    asyncio.run(main(console=True))