#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import math
from pathlib import Path
import time
from filetype import FileType
from filecleaner import FileCleaner

@dataclass
class File:
    """A class to represent a file."""

    # Attributes
    path: Path
    name: str = None
    clean_name = None
    stem: str = None
    clean_stem: str = None
    extension: str = None
    size: int = None
    modification_time: float = None
    file_type: FileType = None

    # Special methods

    def __post_init__(self):
        """
        Initializes the file attributes.
        """
        # Ensure the path exists and is a file
        if not self.path.exists():
            raise FileNotFoundError(f"The file {self.path} does not exist.")

        if not self.path.is_file():
            raise ValueError(f"The path {self.path} is not a file.")

        # Resolve the path to its absolute form
        self.path = self.path.resolve()

        # Set the file attributes
        self.name = self.path.name
        self.clean_name = FileCleaner.get_cleaned_file_name(self.path)
        self.stem = self.path.stem
        self.clean_stem = FileCleaner.get_cleaned_file_stem(self.path)
        self.extension = self.path.suffix[1:].lower()  # Remove leading dot and convert to lowercase
        self.size = self.path.stat().st_size / (1024 * 1024) # Convert size to MB
        self.modification_time = self.path.stat().st_mtime
        self.file_type = FileType.get(self.path)

    def __del__(self):
        """
        Frees the resources used by the file.
        """
        del self.path
        del self.name
        del self.clean_name
        del self.stem
        del self.clean_stem
        del self.extension
        del self.size
        del self.modification_time
        del self.file_type

    def __hash__(self) -> int:
        """
        Returns the hash of the file based on its stem.
        """
        return hash(self.stem)

    def __str__(self) -> str:
        return (f"File: {self.path}\n"
                f"Name: {self.name}\n"
                f"Extension: {self.extension}\n"
                f"Size: {self.human_readable_size()}\n"
                f"Last Modified: {self.formatted_modification_time()}\n"
                f"Type: {self.file_type.value}")
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the file.
        """
        return f"File({self.path!r})"
    
    def __eq__(self, other: 'File') -> bool:
        """
        Checks if two files are equal based on their stems.

        :param other: The other file to compare.
        :return: True if the files are equal, False otherwise.
        """
        return self.stem == other.stem 
    
    def __ne__(self, other: 'File') -> bool:
        """
        Checks if two files are not equal based on their stems.

        :param other: The other file to compare.
        :return: True if the files are not equal, False otherwise.
        """
        return self.stem != other.stem
    
    def __lt__(self, other: 'File') -> bool:
        """
        Compares two files based on their size.

        :param other: The other file to compare.
        :return: True if the file is smaller than the other file, False otherwise.
        """
        return self.size < other.size
    
    def __le__(self, other: 'File') -> bool:
        """
        Compares two files based on their size.

        :param other: The other file to compare.
        :return: True if the file is smaller than or equal to the other file, False otherwise.
        """
        return self.size <= other.size
    
    def __gt__(self, other: 'File') -> bool:
        """
        Compares two files based on their size.

        :param other: The other file to compare.
        :return: True if the file is larger than the other file, False otherwise.
        """
        return self.size > other.size
    
    def __ge__(self, other: 'File') -> bool:
        """
        Compares two files based on their size.

        :param other: The other file to compare.
        :return: True if the file is larger than or equal to the other file, False otherwise.
        """
        return self.size >= other.size
    
    def __len__(self) -> int:
        """
        Returns the size of the file.
        """
        return self.size
    
    def __bool__(self) -> bool:
        """
        Returns True if the file exists and has a size greater than 0, False otherwise.
        """
        return self.path.exists() and self.size > 0
    
    def __add__(self, other: 'File') -> int:
        """
        Adds the size of two files.

        :param other: The other file to add.
        :return: The sum of the sizes of the two files.
        """
        return self.size + other.size
    
    def __sub__(self, other: 'File') -> int:
        """
        Subtracts the size of two files.

        :param other: The other file to subtract.
        :return: The difference of the sizes of the two files.
        """
        return self.size - other.size
        """
        Not implemented.
        """
        raise NotImplementedError("Bitwise inversion is not supported for files.")
    
    def __neg__(self) -> int:
        """
        Returns the negative size of the file.
        """
        return -self.size
    
    def __pos__(self) -> int:
        """
        Returns the positive size of the file.
        """
        return +self.size
    
    def __abs__(self) -> int:
        """
        Returns the absolute size of the file.
        """
        return abs(self.size)
    
    def __round__(self, n: int = 0) -> int:
        """
        Rounds the size of the file to the nearest integer.
        """
        return round(self.size, n)
    
    def __floor__(self) -> int:
        """
        Returns the floor of the size of the file.
        """
        return math.floor(self.size)
    
    def __ceil__(self) -> int:
        """
        Returns the ceiling of the size of the file.
        """
        return math.ceil(self.size)

    def __contains__(self, item: str) -> bool:
        """
        Checks if a string is contained in the file name.

        :param item: The string to search for.
        :return: True if the string is contained in the file name, False otherwise.
        """
        return item in self.stem
    
    # Public methods

    def human_readable_size(self) -> str:
        """
        Converts the file size into a human-readable format.
        """
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']:
            if size < 1024 or unit == 'EB':
                return f"{size:.2f} {unit}"
            size /= 1024

    def formatted_modification_time(self) -> str:
        """
        Formats the modification time into a human-readable string.
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.modification_time))

    def reload(self):
        """
        Reloads the file attributes.
        """
        try:
            self.__post_init__()
        except FileNotFoundError as e:
            print(f"Error reloading file: {e}")
