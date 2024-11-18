#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from enum import Enum
from pathlib import Path
from .file_type import FileType
from .file_system_node import FileSystemNode
from .file_system_node_factory import FileSystemNodeFactory
from .node_name_cleaner import NodeNameCleaner
from .directory import Directory
from .file import File
from termcolor import colored

class Colors(Enum):
    GREY = 'grey'
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'
    MAGENTA = 'magenta'
    CYAN = 'cyan'
    WHITE = 'white'

class FileSorter:
    """
    A class to sort files corresponding directories based on their filename and extension.
    The class can clean filenames, pack files into directories, and sort them accordingly.
    """
    
    # Directories by file type
    SORTED_DIR = {
        FileType.MOVIE: "001-MOVIES",
        FileType.TVSHOW: "002-TVSHOWS",
        FileType.EBOOK: "003-EBOOKS",
        FileType.AUDIO: "004-AUDIO",
        FileType.APP: "005-APPS",
        FileType.ANDROID: "006-ANDROID",
        FileType.SCRIPT: "099-SCRIPTS",
    }

    # Allowed file types for directory sorting
    ALLOWED_TYPES = {
        FileType.MOVIE: [FileType.SUBTITLE],
        FileType.TVSHOW: [FileType.MOVIE, FileType.SUBTITLE],
        FileType.EBOOK: [],
        FileType.AUDIO: [],
        FileType.APP: [],
        FileType.IMAGE: [],
        FileType.ISO: [],
        FileType.ANDROID: [],
        FileType.SCRIPT: [],
    }
    
    # Constructor
    
    def __init__(self, root_node: FileSystemNode, verbose: bool = False, dry_run: bool = False):
        """
        Initializes the FileSorter object.
        :param root_node: The root node to sort.
        :param verbose: True for verbose output, False otherwise. (default is False)
        :param dry_run: True for dry run, False otherwise. (default is False)
        """
        self.root_node = root_node
        self.verbose = verbose
        self.dry_run = dry_run
    
    # Private methods
    
    def __check_node_type(self, node: FileSystemNode) -> FileType|None:
        """
        Checks if the node type is allowed for sorting.
        :param node: The node to check.
        :return: The file type of the node, 
        """
        # Get the node type
        node_type = node.get_type()
        
        # Verbosity
        if self.verbose:
            print(colored(f"Node type: {node_type}", Colors.YELLOW.value))
        
        # Check if the file type is not allowed
        if not node_type in FileSorter.ALLOWED_TYPES.keys():
            # Verbosity
            if self.verbose:
                print(colored(f"File type {node_type} is not allowed.", Colors.RED.value))
            return None
        
        # Check if there is a sorted directory for the file type
        if node_type not in FileSorter.SORTED_DIR.keys():
            # Verbosity
            if self.verbose:
                print(colored(f"No sorted directory for file type {node_type}", Colors.RED.value))
            return None
        
        return node_type
        
    def __is_sorted_dir(self, node: FileSystemNode) -> bool:
        """
        Determines if a directory is a sorted directory.

        :param node: FileSystem node to check.
        :return: True if the directory is a sorted directory, False otherwise.
        """
        if not node._is(Directory):
            return False
        return any([node.name == sorted_dir for sorted_dir in FileSorter.SORTED_DIR.values()])
    
    def __get_sorted_dir(self, node: FileSystemNode) -> Path:
        """
        Gets the sorted directory path for a node based on its type.
        :param node: The node to get the destination path for.
        :return: The sorted directory path.
        """
        
        # Get the file type of the node
        file_type = node.get_type()
        
        # Get the sorted directory for the file type
        sorted_dir = node.parent.joinpath(FileSorter.SORTED_DIR[file_type])
        
        # Check if the sorted directory exists
        if not sorted_dir.exists():
            raise FileNotFoundError(f"The sorted directory {sorted_dir} does not exist.")
        
        return sorted_dir
    
    def __get_node_destination(self, node: FileSystemNode) -> Path:
        """
        Gets the destination path for a node based on its type.
        :param node: The node to get the destination path for.
        :return: The destination path.
        """
        # Get the sorted directory for the node
        sorted_dir = self.__get_sorted_dir(node)
        
        # Node type
        node_type = node.get_type()
        
        # Check if the node is a MOVIE
        if node_type == FileType.MOVIE:
            if node._is(File):
                # Movie year
                movie_year = NodeNameCleaner.get_year_from_node_name(node.stem_cleaned)
                if movie_year is not None:
                    # Movie folder name with the year in parentheses
                    movie_folder_name = f"{NodeNameCleaner.get_name_without_year(node.stem_cleaned)} ({movie_year})"
                else:
                    # Movie folder name without the year
                    movie_folder_name = node.stem_cleaned
                # Destination is a directory with the same name as the node in the sorted directory
                return sorted_dir / movie_folder_name
            else:
                # Destination is a directory with the same name as the node in the sorted directory
                return sorted_dir
        
        # Check if the node is a TVSHOW
        if node_type == FileType.TVSHOW:
            # Destination is a directory with the same name as the node in the sorted directory
            return sorted_dir / NodeNameCleaner.get_name_without_season_and_episode(node.stem_cleaned)

        # default
        return sorted_dir
        
    # Public methods

    def sort(self, node: FileSystemNode) -> None:
        """
        Sorts nodes into either the corresponding file type directory.
        :param node: The node to sort.
        :return: None
        """
        
        # Verbosity
        if self.verbose:
            # Separator
            print(colored("-" * 100, Colors.WHITE.value, attrs=["bold"]))
            print(colored(f"Sorting node: {node}", Colors.YELLOW.value))

        # Check if the node is sorted directory
        if self.__is_sorted_dir(node):
            # Verbosity
            if self.verbose:
                print(colored(f"Node {node} is a sorted directory.", Colors.CYAN.value))
            return
        
        # Get the node type
        node_type = self.__check_node_type(node)
        
        # Verbosity
        if node_type is None:
            return
        
        # Get the sorted directory for the file type
        sorted_dir = node.parent.joinpath(FileSorter.SORTED_DIR[node_type])
        
        # Check if the sorted directory exists
        if not sorted_dir.exists():
            raise FileNotFoundError(f"The sorted directory {sorted_dir} does not exist.")
        
        
        # Get the destination path for the node
        destination = self.__get_node_destination(node)
        
        # Verbosity
        if self.verbose:
            print(colored(f"Cleaned node name: {node.name_cleaned}", Colors.YELLOW.value))
            print(colored(f"Sorted directory: {sorted_dir}", Colors.YELLOW.value))
            print(colored(f"Destination: {destination / node.name_cleaned}", Colors.GREEN.value))
        
        # Move the node to the sorted directory
        if not self.dry_run:
            node.move(destination / node.name_cleaned)

    def process(self) -> None:
        """
        Processes a node by sorting it into the corresponding directory.
        :return: None
        """
        
        # Verbosity
        if self.verbose:
            print(colored(f"Processing node: {self.root_node}", Colors.YELLOW.value))
            # Get node class name
            print(colored(f"Class: {self.root_node.__class__.__name__}", Colors.YELLOW.value))
        
        # Check if the root node is a file
        if self.root_node._is(File):
            # Verbosity
            if self.verbose:
                print(colored(f"Processing file: {self.root_node}", Colors.BLUE.value))
            self.sort(self.root_node)
            return
        
        # Check if the root node is a directory
        if self.root_node._is(Directory):
            # Verbosity
            if self.verbose:
                print(colored(f"Processing directory: {self.root_node}", Colors.GREY.value))
            # Process each child node
            for node in self.root_node:
                self.sort(node)
            return
        
        # Error
        raise ValueError(f"Node type {self.root_node} is not allowed.")