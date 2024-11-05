#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import os
import re
import shutil
from collections import Counter
from typing import Iterator
from .file_system_node import FileSystemNode
from .file import File
from .file_type import FileType

@dataclass
class Directory(FileSystemNode):

    """ A class to represent a directory. """

    # Attributes specific to the directory

    year: int = field(init=False)
    recursive: bool = field(default=False)

    # Special methods
    
    # - Initialization and deletion

    def __post_init__(self) -> None:
        """
        Initializes the directory attributes.
        """
        # Superclass initialization
        super().__post_init__()
        # Ensure node is a directory
        if not self.path.is_dir():
            raise ValueError(f"The path {self.path} is not a directory.")
        # Stem is the name without year in parentheses
        self.stem = self.name.split(' (')[0]
        # Year is the year in parentheses if it exists at the end of the name and is a 4-digit number else 0
        self.year = 0
        match = re.search(r'\((\d{4})\)$', self.name)
        if match:
            self.year = int(match.group(1))
            # Update stem to exclude the year
            self.stem = self.name[:match.start()].strip()

    def __del__(self) -> None:
        """
        Frees the resources used by the directory.
        Examples: del dir frees the resources used by the directory.
        """
        super().__del__()
        del self.year
        del self.recursive

    # - String representation
    
    def __str__(self) -> str:
        """
        Returns a string representation of the directory.
        Examples: str(dir) returns a string representation of the directory.
        :return: A string representation of the directory.
        """
        return (f"Directory: {self.path}\n"
                f"Name: {self.name}\n"
                f"Stem: {self.stem}\n"
                f"Year: {self.year}\n"
                f"Size: {self.human_readable_size()}\n"
                f"Items: {self.count()}\n"
                f"  - Files: {self.count_files()}\n"
                f"  - Subdirectories: {self.count_dirs()}\n"
                f"Recursive: {self.recursive}\n"
                f"Last Modified: {self.formatted_modification_time()}\n"
                f"Type: {self.get_type()}")
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the directory.
        Examples: repr(dir) returns a string representation of the directory.
        :return: A string representation of the directory.
        """
        return f"Directory({self.path})"

    # - Iteration and containment
    
    def __iter__(self) -> Iterator[FileSystemNode]:
        """
        Returns an iterator over the contents of the directory.
        Example: iter(dir) returns an iterator over the nodes of the directory.
        """
        return self.__get_content(recursive=self.recursive)
    
    def __next__(self) -> FileSystemNode:
        """
        Returns the next node in the directory.
        Example: next(dir) returns the next node in the directory.
        """
        return next(self.__get_content(recursive=self.recursive))
    
    def __contains__(self, node: FileSystemNode) -> bool:
        """
        Checks if an node is in the directory.
        Example: file in dir checks if the file is in the directory.
        :param node: The node to check.
        :return: True if the node is in the directory, False otherwise.
        """
        # Check if item is in the current directory
        if node in os.listdir(self.path):
            return True
        
        # If recursive is True, check subdirectories
        if self.recursive:
            for root, dirs, files in os.walk(self.path):
                if node in files or node in dirs:
                    return True
        return False
    
    def __getitem__(self, search: str) -> FileSystemNode:
        """
        Gets an item from the directory by name or hash.
        Example: dir['file.txt'] gets the file 'file.txt' from the directory.
        :param search: The name or hash of the item to get.
        :return: The node in the directory.
        """
        for node in self.__get_content(recursive=self.recursive):
            if node.name == search or hash(node) == search:
                return node
        raise KeyError(f"No node {search} in the directory {self.path}")
    
    def __setitem__(self, search: str, new_node: FileSystemNode) -> None:
        """
        Replaces an node in the directory.
        Example: dir['file.txt'] = new_file replaces the file 'file.txt' with new_file in the directory
        :param search: The name or hash of the node to replace.
        :param new_node: The new node to replace the old node
        """
        for node in self.__get_content(recursive=self.recursive):
            if node.name == search or hash(node) == search:
                node.path.rename(new_node.path)
                return
        raise KeyError(f"No node {search} in the directory {self.path}")
    
    def __delitem__(self, search: str) -> None:
        """
        Deletes an node from the directory.
        Example: del dir['file.txt'] deletes the file 'file.txt' from the directory.
        :param search: The name or hash of the node to delete.
        """
        for node in self.__get_content(recursive=self.recursive):
            if node.name == search or hash(node) == search:
                # Check if the node is a file or a directory
                if node.path.is_dir():
                    # Delete the directory recursively
                    shutil.rmtree(node.path)
                else:
                    # Delete the file
                    node.path.unlink()
                return
        raise KeyError(f"No node {search} in the directory {self.path}")
        
    # - File and directory operations via mathematical operators
    
    def __pow__(self, other: 'Directory') -> 'Directory':
        """
        Merges two directories.
        Moves all files and subdirectories from the other directory to the current directory, then deletes the other directory.
        Example: dir1 ** dir2 merges the contents of dir2 into dir1.
        :param other: The other directory to merge.
        :return: The current directory with the merged contents.
        """
        for item in other:
            item.path.rename(self.path / item.name)
        other.path.rmdir()
        return self
    
    def __mod__(self, other: str) -> 'Directory':
        """
        Creates a subdirectory in the directory.
        Example: dir % 'subdir' creates a subdirectory named 'subdir' in the directory 'dir'.
        :param other: The name of the subdirectory to create.
        :return: A Directory instance for the new subdirectory.
        """
        new_dir = self.path / other
        new_dir.mkdir()
        return Directory(new_dir)
    
    def __and__(self, other: 'Directory') -> set:
        """
        Creates a set intersection of two directories contents.
        Example: dir1 & dir2 returns a set of files and directories that are in both dir1 and dir2.
        :param other: The other directory to compare.
        :return: A set of files and directories that are in both directories.
        """
        return set(self.__get_content(recursive=self.recursive)) & set(other.__get_content(other.recursive))
    
    def __or__(self, other: 'Directory') -> 'Directory':
        """
        Combines two directories.
        A set union of two sets is the set of elements that are in either of the sets.
        Example: dir1 | dir2 combines the contents of dir1 and dir2.
        :param other: The other directory to combine.
        :return: A directory with the combined contents of the two directories.
        """
        return set(self) | set(other)
    
    def __invert__(self) -> 'Directory':
        """
        Inverts the directory contents.
        A set difference of two sets is the set of elements that are in the first set, but not in the second set.
        Example: ~dir inverts the contents of the directory.
        :return: A directory with the inverted contents.
        """
        return set(self) ^ set(self)

    # Private methods

    def __get_content(self, recursive: bool = True) -> Iterator[FileSystemNode]:
        """
        Generator that yields FileSystemNode instances for the contents of the directory.

        :param recursive: If True, recursively includes contents of subdirectories.
        :yield: An iterator over FileSystemNode instances.
        """
        if recursive:
            nodes_iterator = self.path.rglob('*')
        else:
            nodes_iterator = self.path.iterdir()

        for node_path in nodes_iterator:
            if node_path.is_file():
                try:
                    yield File(node_path)
                except (FileNotFoundError, ValueError) as e:
                    print(f"Error processing file {node_path}: {e}")
            elif node_path.is_dir():
                try:
                    yield Directory(node_path)
                except (FileNotFoundError, ValueError) as e:
                    print(f"Error processing directory {node_path}: {e}")

    def __get_directories(self, recursive: bool = True) -> Iterator['Directory']:
        """
        Generator that yields Directory instances for all subdirectories in the directory.

        :param recursive: If True, recursively includes subdirectories of subdirectories.
        :yield: An iterator over Directory instances.
        """
        if recursive:
            dirs_iterator = self.path.rglob('*')
        else:
            dirs_iterator = self.path.iterdir()

        for dir_path in dirs_iterator:
            if dir_path.is_dir():
                try:
                    yield Directory(dir_path)
                except (FileNotFoundError, ValueError) as e:
                    print(f"Error processing directory {dir_path}: {e}")
    
    def __get_files(self, recursive: bool = True) -> Iterator[File]:
        """
        Generator that yields File instances for all files in the directory.

        :param recursive: If True, recursively includes files in subdirectories.
        :yield: An iterator over File instances.
        """
        if recursive:
            files_iterator = self.path.rglob('*')
        else:
            files_iterator = self.path.iterdir()

        for file_path in files_iterator:
            if file_path.is_file():
                try:
                    yield File(file_path)
                except (FileNotFoundError, ValueError) as e:
                    print(f"Error processing file {file_path}: {e}")

    # Public methods
    
    def get_type(self) -> FileType:
        """
        Gets the type of the directory based on its contents.
        :return: The FileType of the directory
        """
        file_types = Counter([file.get_type() for file in self.__get_files()])
        if file_types:
            return max(file_types, key=file_types.get)
        return FileType.OTHER
        
    def count(self) -> int:
        """
        Returns the number of nodes in the directory.
        :return: The number of nodes in the directory.
        """
        return sum(1 for _ in self.__get_content(recursive=False))
    
    def count_dirs(self) -> int:
        """
        Returns the number of subdirectories in the directory.
        :return: The number of subdirectories in the directory.
        """
        return sum(1 for _ in self.__get_directories(recursive=False))
    
    def count_files(self) -> int:
        """
        Returns the number of files in the directory.
        :return: The number of files in the directory.
        """
        return sum(1 for _ in self.__get_files(recursive=False))
    


