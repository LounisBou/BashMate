#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from pymate import LogIt

from filemate.directory import Directory
from filemate.file import File
from filemate.file_system_node import FileSystemNode
from filemate.file_type import FileType
from filemate.node_name_cleaner import NodeNameCleaner


@dataclass
class Sorter:
    """
    A class to sort nodes corresponding directories based on their name and extension.
    The class can clean names, pack nodes into sorted directories.
    """
    
    # Attributes & initialization
    
    root_node: FileSystemNode = field(init=True, metadata={"help": "The root node to sort."})
    verbose: bool = field(init=True, default=False, metadata={"help": "True for verbose output, False otherwise."})
    dry_run: bool = field(init=True, default=False, metadata={"help": "True for dry run, False otherwise."})
    sorted_dir_names: dict = field(init=False, default_factory=dict, metadata={"help": "Sorted directories by file type."})
    allowed_types: dict = field(init=False, default_factory=dict, metadata={"help": "Allowed types for each file type."})
    logger: LogIt = field(init=True, default_factory=LogIt, metadata={"help": "The logger."})
    name_cleaner: NodeNameCleaner = field(init=False, default_factory=NodeNameCleaner, metadata={"help": "The node name cleaner."})
    
    def __post_init__(self):
        """
        Post initialization method.
        """
        # Defined sorted directories
        self.__defined_sorted_dir()
        # Defined allowed types
        self.__defined_allowed_types()
    
    # Private methods
    
    def __defined_sorted_dir(self) -> bool:
        """
        Import sorted directories names from .env file.
        """
        load_dotenv()
        # Directories by file type
        self.sorted_dir_names = {
            FileType.MOVIE: os.getenv("MOVIE_DIR"),
            FileType.TVSHOW: os.getenv("TVSHOW_DIR"),
            FileType.EBOOK: os.getenv("EBOOK_DIR"),
            FileType.AUDIO: os.getenv("AUDIO_DIR"),
            FileType.APP: os.getenv("APP_DIR"),
            FileType.IMAGE: os.getenv("IMAGE_DIR"),
            FileType.ISO: os.getenv("ISO_DIR"),
            FileType.ANDROID: os.getenv("ANDROID_DIR"),
            FileType.SCRIPT: os.getenv("SCRIPT_DIR"),
        }
        
    def __defined_allowed_types(self) -> bool:
        """
        Define allowed types for each file type.
        """
        self.allowed_types = {
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
    
    def __check_node_type(self, node: FileSystemNode) -> FileType|None:
        """
        Checks if the node type is allowed for sorting.
        :param node: The node to check.
        :return: The file type of the node, 
        """
        # Get the node type
        node_type = node.get_type()
        
        # Check if the file type is not allowed
        if node_type not in self.allowed_types:
            # Logging
            self.logger.warning(f"File type {node_type} is not allowed.")
            return None
        
        # Check if there is a sorted directory for the file type
        if node_type not in self.sorted_dir_names:
            # Logging
            self.logger.warning(f"No sorted directory for file type {node_type}")
            return None
        
        return node_type
        
    def __is_sorted_dir(self, node: FileSystemNode) -> bool:
        """
        Determines if a directory is a sorted directory.

        :param node: FileSystem node to check.
        :return: True if the directory is a sorted directory, False otherwise.
        """
        if not node.is_instance(Directory):
            return False
        return any([node.name == sorted_dir for sorted_dir in self.sorted_dir_names.values()])
    
    def __get_sorted_dir_node(self, node: FileSystemNode) -> FileSystemNode:
        """
        Gets the sorted directory path for a node based on its type.
        :param node: The node to get the destination path for.
        :return: The sorted directory path.
        """
        
        # Get the file type of the node
        file_type = node.get_type()
        
        # Get the sorted directory name as string
        sorted_dir_name = self.sorted_dir_names[file_type]
        
        # Get the sorted directory for the file type
        sorted_dir = self.root_node / sorted_dir_name
        
        return sorted_dir
    
    def __get_node_destination_path(self, node: FileSystemNode) -> Path:
        """
        Gets the destination path for a node based on its type.
        :param node: The node to get the destination path for.
        :return: The destination Path.
        """
        # Get the sorted Directory for the node
        sorted_dir = self.__get_sorted_dir_node(node)
        
        # Node type
        node_type = node.get_type()
        
        # Check if the sorted directory exists
        if sorted_dir is None:
            self.logger.warning(f"Sorted directory for type {node_type.value} does not exist.")
            return None
        
        # Check if the node is a MOVIE
        if node_type == FileType.MOVIE:
            # Movie year
            movie_year = self.name_cleaner.get_year_from_node_name(node.stem_cleaned)
            if movie_year is not None:
                # Movie folder name with the year in parentheses
                movie_folder_name = f"{self.name_cleaner.get_name_without_year(node.stem_cleaned)} ({movie_year})"
            else:
                # Movie folder name without the year
                movie_folder_name = node.stem_cleaned
            if node.is_instance(File):
                # Destination is a directory with the same name as the node in the sorted directory
                return sorted_dir.path / movie_folder_name.capitalize()
            else:
                # If not dry run
                if not self.dry_run:
                    # Rename the directory node directly 
                    node.rename(movie_folder_name.capitalize())
                else:
                    # Print
                    self.logger.warning(f"Renaming movie dir to : {movie_folder_name.capitalize()}")
                # Destination is a directory with the same name as the node in the sorted directory
                return sorted_dir.path
        
        # Check if the node is a TVSHOW
        if node_type == FileType.TVSHOW:
            # Create TVSHOW directory
            tvshow_dir = self.name_cleaner.get_name_without_season_and_episode(node.stem_cleaned)
            tvshow_dir = self.name_cleaner.get_name_without_year(tvshow_dir)
            tvshow_dir = tvshow_dir.capitalize()
            # Destination is a directory with the same name as the node in the sorted directory
            return sorted_dir.path / tvshow_dir
            

        # default
        return sorted_dir.path
    
    def __get_node_elements_to_sort(self, node: FileSystemNode, node_type: FileType) -> list[FileSystemNode]|None:
        """
        Get the elements of a node to sort.
        :param node: The node to get the elements for.
        :param node_type: The type of the node.
        :return: A list of elements for the node, None if the element to sort is the node itself.
        """
        # Check if the node is a file
        if node.is_instance(File):
            return None
        
        # Check node type
        
        # - TVSHOW
        if node_type == FileType.TVSHOW:
            elements = []
            for child_node in node:
                if child_node.get_type() == FileType.TVSHOW:
                    elements.append(child_node)
            return elements
        
        # All other cases
        return None
                
        
    # Public methods
    
    def set_allowed_types(self, file_type: FileType, allowed_types: list[FileType]) -> None:
        """
        Set the allowed types for a file type.
        :param file_type: The file type to set the allowed types for.
        :param allowed_types: The allowed types for the file type.
        :return: None
        """
        self.allowed_types[file_type] = allowed_types

    def sort(self, node: FileSystemNode, delete_remaining_element: bool = False) -> None:
        """
        Sorts nodes into either the corresponding file type directory.
        :param node: The node to sort.
        :param delete_remaining_element: True to delete the remaining element, False otherwise.
        :return: None
        """

        # Check if the node is sorted directory
        if self.__is_sorted_dir(node):
            return
        
        # Logging
        self.logger.separator()
        self.logger.show(f"Sorting node: {node}")
        
        # Get the node type
        node_type = self.__check_node_type(node)
        if node_type is None:
            return
        
        # Logging
        self.logger.info(f"Node type: {node_type}")
        
        # Get the sorted directory for the file type
        sorted_dir = node.parent.joinpath(self.sorted_dir_names[node_type])
        
        # Get the destination path for the node
        destination_path = self.__get_node_destination_path(node)
        if destination_path is None:
            return
        
        # Logging
        self.logger.info(f"Cleaned node name: {node.name_cleaned}")
        self.logger.info(f"Sorted directory: {sorted_dir}")
        self.logger.info(f"Destination path: {destination_path}")
            
        # Elements to sort
        elements = self.__get_node_elements_to_sort(node, node_type)
        if elements is not None:
            for element in elements:
                # Logging
                self.logger.success(f"Node to sort: [{element.__class__.__name__}] {destination_path / element.name_cleaned}")
                # Move the node to the sorted directory
                if not self.dry_run:
                    element.move(destination_path / element.name_cleaned)
            # Delete remaining element
            if delete_remaining_element:
                # Logging
                self.logger.warning(f"Deleting remaining element: {node}")
                if not self.dry_run:
                    # Delete remaining node
                    node.delete(recursive=True)
        else:
            # Logging
            self.logger.success(f"Node to sort: [{node.__class__.__name__}] {destination_path / node.name_cleaned}")
            # Move the node to the sorted directory
            if not self.dry_run:
                node.move(destination_path / node.name_cleaned)
                
        

    def process(self, delete_remaining_element: bool = False) -> None:
        """
        Processes a node by sorting it into the corresponding directory.
        :param delete_remaining_element: True to delete the remaining element, False otherwise.
        :return: None
        """
        
        # Check if the root node is a file
        if self.root_node.is_instance(File):
            # Check if verbose is enabled
            if self.verbose:
                self.logger.show(f"Sorting file: {self.root_node.name_cleaned}")
            self.sort(self.root_node)
            return
        
        # Check if the root node is a directory
        if self.root_node.is_instance(Directory):
            # Check if verbose is enabled
            if self.verbose:
                self.logger.show(f"Sorting directory: {self.root_node.name_cleaned}")
            # Process each child node
            for node in self.root_node:
                # Check if verbose is enabled
                if self.verbose:
                    self.logger.show(f"Sorting child node: {node.name_cleaned}")
                # Sort the node
                self.sort(node, delete_remaining_element)
            return
        
        # Error
        raise ValueError(f"Node type {self.root_node} is not allowed.")