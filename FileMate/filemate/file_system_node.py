#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import math
from pathlib import Path
from dataclasses import dataclass, field
import shutil
import time
from filemate.node_name_cleaner import NodeNameCleaner


@dataclass
class FileSystemNode(ABC):
    """
    A class to represent a fileSystem node.
    """

    # Attributes
    
    path: Path
    name: str = field(init=False, default="", metadata="The name of the node.")
    name_cleaned: str = field(init=False, default="", metadata="The cleaned name of the node.")
    stem: str = field(init=False, default="", metadata="The name of the node, without the extension.")
    stem_cleaned: str = field(init=False, default="", metadata="The cleaned name of the node, without the extension.")
    size: int = field(init=False, default=0, metadata="The size of the node.")
    modification_time: float = field(init=False, default=0, metadata="The last modification time of the node.")
    name_cleaner: NodeNameCleaner = field(init=False, default_factory=NodeNameCleaner, metadata="The node name cleaner.")
    
    # Special methods
    
    # - Initialization and deletion

    def __post_init__(self) -> None:
        """
        Sets the attributes of the node.
        """
        if not isinstance(self.path, Path):
            raise TypeError("path must be a pathlib.Path instance")
        if not self.path.exists():
            raise FileNotFoundError(f"The node {self.path} does not exist.")
        # Set the directory attributes
        self.path = self.path.resolve()
        self.parent = self.path.parent.resolve()
        self.name = self.path.name
        self.name_cleaned = self.name_cleaner.get_cleaned_node_name(self.path)
        self.stem = self.path.stem
        self.stem_cleaned = self.name_cleaner.get_cleaned_node_stem(self.path)
        self.modification_time = self.path.stat().st_mtime # last modification time

    # - Class check
    
    def is_instance(self, node: 'FileSystemNode') -> bool:
        """
        Checks if the node is an instance of the given class.
        Example: node.is(File)
        :param object: The class to check.
        :return: True if the node is an instance of the given class, False otherwise.
        """
        return isinstance(self, node)
    
    def _instanceof(self) -> 'FileSystemNode':
        """
        Returns the class of the node
        Example: node.instanceof()
        :return: The class of the node
        """
        # Check if the node is a FileSystemNode
        if isinstance(self, FileSystemNode):
            return self.__class__
        # If the node is not a FileSystemNode, raise an error
        raise ValueError("The node is not an instance of File or Directory.")
    
    # - Comparison
        
    def __hash__(self) -> int:
        """
        Returns the hash of the node based on its name.
        Example: hash(node)
        """
        return hash(self.name)
    
    def __eq__(self, other: 'FileSystemNode') -> bool:
        """
        Checks if two nodes are equal based on their names.
        Examples: node1 == node2
        """
        return self.name == other.name
    
    def __ne__(self, other: 'FileSystemNode') -> bool:
        """
        Checks if two nodes are not equal based on their names.
        Examples: node1 != node2
        """
        return self.name != other.name
    
    # - Size comparison and operations

    def __add__(self, other: 'FileSystemNode') -> int:
        """
        Adds the size of two node.
        Example: file1 + file2
        :param other: The other node to add.
        :return: The sum of the sizes of the two nodes.
        """
        return self.size + other.size
    
    def __sub__(self, other: 'FileSystemNode') -> int:
        """
        Subtracts the size of two nodes.
        Example: file1 - file2
        :param other: The other node to subtract.
        :return: The difference of the sizes of the two nodes.
        """
        return self.size - other.size
    
    def __len__(self) -> int:
        """
        Returns the size of the node.
        Example: len(node)
        :return: The size of the node.
        """
        return self.size
    
    def __lt__(self, other: 'FileSystemNode') -> bool:
        """
        Compares two nodes based on their size.
        Example: node1 < node2
        :param other: The other node to compare.
        :return: True if the node is smaller than the other node, False otherwise.
        """
        return self.size < other.size
    
    def __le__(self, other: 'FileSystemNode') -> bool:
        """
        Compares two nodes based on their size.
        Example: node1 <= node2
        :param other: The other node to compare.
        :return: True if the node is smaller than or equal to the other node, False otherwise.
        """
        return self.size <= other.size
    
    def __gt__(self, other: 'FileSystemNode') -> bool:
        """
        Compares two nodes based on their size.
        Example: node1 > node2
        :param other: The other node to compare.
        :return: True if the node is larger than the other node, False otherwise.
        """
        return self.size > other.size
    
    def __ge__(self, other: 'FileSystemNode') -> bool:  
        """
        Compares two nodes based on their size.
        Example: node1 >= node2
        :param other: The other node to compare.
        :return: True if the node is larger than or equal to the other node, False otherwise.
        """
        return self.size >= other.size
    
    def __neg__(self) -> int:
        """
        Return the negative size of the directory.
        Example: -node returns the negative size of the directory.
        :return: The negative size of the directory.
        """
        return -self.size
    
    def __pos__(self) -> int:
        """
        Return the positive size of the directory.
        Example: +node returns the positive size of the directory.
        :return: The positive size of the directory.
        """
        return +self.size
    
    def __abs__(self) -> int:
        """
        Return the absolute size of the directory.
        Example: abs(node) returns the absolute size of the directory.
        :return: The absolute size of the directory.
        """
        return abs(self.size)
    
    def __round__(self, n: int = 0) -> int:
        """
        Rounds the size of the directory.
        Example: round(node, 2) rounds the size of the directory to 2 decimal places.
        :param n: The number of decimal places to round to. Default is 0.
        :return: The rounded size of the directory.
        """
        return round(self.size, n)
    
    def __floor__(self) -> int:
        """
        Returns the floor value of the size of the directory.
        Example: floor(node) returns the floor value of the size of the directory.
        :return: The floor value of the size of the directory.
        """
        return math.floor(self.size)
    
    def __ceil__(self) -> int:
        """
        Returns the ceiling value of the size of the directory.
        Example: ceil(node) returns the ceiling value of the size of the directory.
        :return: The ceiling value of the size of the directory.
        """
        return math.ceil(self.size)
        
    # - Existence check
    
    def __bool__(self) -> bool:
        """
        Checks if the node exists and has a size greater than 0.
        Example: if node:
        :return: True if the node exists and has a size greater than 0, False otherwise
        """
        return self.path.exists() and self.size > 0
    
    # - String representation
    
    @abstractmethod
    def __str__(self) -> str:
        """
        Returns the string representation of the node.
        Example: str(node)
        :return: The string representation of the node.
        """
        raise NotImplementedError("The __str__ method must be implemented in the subclass.")
    
    @abstractmethod
    def __repr__(self) -> str:
        """
        Returns the string representation of the node.
        Example: repr(node)
        :return: The string representation of the node.
        """
        raise NotImplementedError("The __repr__ method must be implemented in the subclass.")   
    
    # Private methods
    
    # Public methods
    
    # - Reload and existence check
    def reload(self):
        """
        Reloads the file attributes.
        """
        try:
            self.__post_init__()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {self.path} does not exist.") from e
    
    # - Format conversion
    
    def get_size(self) -> int:
        """
        Gets the size of the node.
        """
        raise NotImplementedError("The get_size method must be implemented in the subclass.")
    
    def human_readable_size(self, unit: str = None) -> str:
        """
        Converts the file size into a human-readable format.
        :param unit: The unit to convert the size to. Default is None.
        :return: The file size in a human-readable format.
        """
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} {unit}"

    def formatted_modification_time(self, datetime_format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """
        Formats the modification time into a human-readable string.
        :param datetime_format: The format of the modification time. Default is '%Y-%m-%d %H:%M:%S'.
        :return: The formatted modification time.
        """
        return time.strftime(datetime_format, time.localtime(self.modification_time))
    
        # - Type checking
    
    # - Type checking
    
    @abstractmethod
    def get_type(self) -> None:
        """
        Gets the type of the node.
        :return: The type of the node.
        """
        raise NotImplementedError("The __get_type method must be implemented in the subclass.")
    
    def is_symlink(self) -> bool:
        """
        Checks if the node is a symbolic link.
        :return: True if the node is a symbolic link, False otherwise.
        """
        return self.path.is_symlink()
    
    def get_year(self) -> int:
        """
        Check if node name contains a year. If it does, return the year. Otherwise, return 0.
        Patern: yyyy
        """
        return self.name_cleaner.get_year_from_node_name(self.path)
                
    # - Path operations
    
    def joinpath(self, *paths) -> Path:
        """
        Joins the node path with the given paths.
        :param paths: The paths to join.
        :return: The joined path.
        """
        return self.path.joinpath(*paths)
    
    def relative_to(self, other: Path) -> Path:
        """
        Returns a relative path to the node from the other path.
        :param other: The other path.
        :return: The relative path to the node from the other path.
        """
        return self.path.relative_to(other)
    
    # - FileSystem operations
    
    def rename(self, new_name: str) -> None:
        """
        Renames the node.
        :param new_name: The new name of the node.
        """
        new_path = self.path.parent.joinpath(new_name)
        self.path.rename(new_path)
        # Update the path
        self.path = new_path
        self.reload()
        
    def move(self, new_path: Path) -> None:
        """
        Moves the node to a new path.
        :param new_path: The new path of the node.
        """
        # Move the node to the new path and create the parent directories if they don't exist
        new_path.parent.mkdir(parents=True, exist_ok=True)
        new_path = new_path.resolve()
        self.path.rename(new_path)
        # Update the path
        self.path = new_path
        self.reload()
        
    def copy(self, new_path: Path) -> None:
        """
        Copies the node to a new path.
        :param new_path: The new path of the node.
        """
        shutil.copy(self.path, new_path)
        
    def delete(self, recursive=False) -> None:
        """
        Deletes the node.
        """
        raise NotImplementedError("The delete method must be implemented in the subclass.")
    
    def create_symlink(self, target: Path, replace: bool = False) -> None:
        """
        Creates a symbolic link to the node.
        :param target: The target of the symbolic link.
        :param replace: True to replace an existing symbolic link, False otherwise.
        """
        if replace:
            self.path.unlink()
        self.path.symlink_to(target)

    # - Cleanup operations
    
    def clean_name(self) -> None:
        """
        Cleans the name of the node.
        """
        new_name = self.name_cleaner.get_cleaned_node_name(self.path)
        self.rename(new_name)
    