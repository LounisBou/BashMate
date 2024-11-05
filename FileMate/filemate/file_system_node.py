#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import math
from pathlib import Path
from dataclasses import dataclass, field
import time

@dataclass
class FileSystemNode(ABC):
    """
    A class to represent a fileSystem node.
    """

    # Attributes
    
    path: Path
    name: str = field(init=False)
    name_cleaned: str = field(init=False)
    stem: str = field(init=False)
    stem_cleaned: str = field(init=False)
    size: int = field(init=False, default=0)
    modification_time: float = field(init=False)
    
    # Special methods
    
    # - Initialization and deletion

    def __post_init__(self) -> None:
        """
        Sets the attributes of the node.
        """
        if not isinstance(self.path, Path):
            raise TypeError("path must be a pathlib.Path instance")
        # Set the directory attributes
        self.path = self.path.resolve()
        self.name = self.path.name
        self.name_cleaned = self.path.name
        self.stem = self.path.stem
        self.stem_cleaned = self.path.stem
        self.modification_time = self.path.stat().st_mtime
        self.size = self.path.stat().st_size / (1024 * 1024)  # Convert size to MB
    
    def __del__(self) -> None:
        """
        Frees the resources used by the node.
        """
        del self.path
        del self.name
        del self.name_cleaned
        del self.stem
        del self.stem_cleaned
        del self.size
        del self.modification_time
        
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
    
    def reload(self):
        """
        Reloads the file attributes.
        """
        try:
            self.__post_init__()
        except FileNotFoundError as e:
            print(f"Error reloading file: {e}")
            
    def exists(self) -> bool:
        """
        Checks if the file exists.
        :return: True if the file exists, False otherwise.
        """
        return self.path.exists()
    
    def human_readable_size(self, force_unit: str = None) -> str:
        """
        Converts the file size into a human-readable format.
        :param unit: The unit to convert the size to. Default is None.
        :return: The file size in a human-readable format.
        """
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size < 1024 or (force_unit and unit == force_unit):
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} {unit}"

    def formatted_modification_time(self, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """
        Formats the modification time into a human-readable string.
        :param format: The format of the modification time. Default is '%Y-%m-%d %H:%M:%S'.
        :return: The formatted modification time.
        """
        return time.strftime(format, time.localtime(self.modification_time))
    
    def is_file(self) -> bool:
        """
        Checks if the node is a file.
        :return: True if the node is a file, False otherwise.
        """
        return self.path.is_file()
    
    def is_dir(self) -> bool:
        """
        Checks if the node is a directory.
        :return: True if the node is a directory, False otherwise.
        """
        return self.path.is_dir()
            
    @abstractmethod
    def get_type(self) -> str:
        """
        Gets the type of the node.
        :return: The type of the node.
        """
        raise NotImplementedError("The __get_type method must be implemented in the subclass.")
        