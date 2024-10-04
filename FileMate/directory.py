#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import os
from pathlib import Path
import shutil
import time
from collections import Counter
from typing import Dict, Iterator, Union
from filetype import FileType
from file import File

@dataclass
class Directory:

    """ A class to represent a directory. """

    # Attributes

    path: Path
    name: str = field(init=False)
    size: int = field(init=False, default=0)
    modification_time: float = field(init=False)
    recursive: bool = field(default=False)

    # Special methods

    def __post_init__(self):
        """
        Initializes the directory attributes.
        """
        # Ensure the path exists and is a directory
        if not self.path.exists():
            raise FileNotFoundError(f"The directory {self.path} does not exist.")
        # Resolve the path to its absolute form
        if not self.path.is_dir():
            raise ValueError(f"The path {self.path} is not a directory.")
        # Set the directory attributes
        self.path = self.path.resolve()
        self.name = self.path.name
        self.modification_time = self.path.stat().st_mtime
        self.size = self.path.stat().st_size / (1024 * 1024)  # Convert size to MB

    def __getattr__(self, name: str) -> Union[int, FileType]:
        """
        Gets special attributes of the directory.
        :param name: The name of the attribute (number_of_subdirectories, number_of_files, type).
        :return: The value of the attribute.
        """
        if name == 'number_of_subdirectories':
            return sum(1 for _ in self.__get_directories(recursive=False))
        if name == 'number_of_files':
            return sum(1 for _ in self.__get_files(recursive=False))
        if name == 'type':
            return self.__get_type()
        raise AttributeError(f"'Directory' object has no attribute '{name}'")

    def __del__(self):
        """
        Frees the resources used by the directory.
        """
        del self.path
        del self.name
        del self.size
        del self.modification_time

    def __str__(self):
        """
        Returns a string representation of the directory.
        """
        return (f"Directory: {self.path}\n"
                f"Name: {self.name}\n"
                f"Size: {self.__human_readable_size()}\n"
                f"Files: {self.number_of_files}\n"
                f"Subdirectories: {self.number_of_subdirectories}\n"
                f"Last Modified: {self.__formatted_modification_time()}\n"
                f"Type: {self.type.value}")
    
    def __repr__(self):
        """
        Returns a string representation of the directory.
        """
        return f"Directory({self.path})"

    def __hash__(self) -> int:
        """
        Returns the hash of the directory based on its name.
        """
        return hash(self.name)
    
    def __eq__(self, other: 'Directory') -> bool:
        """
        Checks if two directories are equal based on their names.
        """
        return self.name == other.name
    
    def __ne__(self, other: 'Directory') -> bool:
        """
        Checks if two directories are not equal based on their names.
        """
        return not self.name == other.name
    
    def __lt__(self, other: 'Directory') -> bool:
        """
        Compares two directories based on their sizes.
        """
        return self.size < other.size
    
    def __le__(self, other: 'Directory') -> bool:
        """
        Compares two directories based on their sizes.
        """
        return self.size <= other.size
    
    def __gt__(self, other: 'Directory') -> bool:
        """
        Compares two directories based on their sizes.
        """
        return self.size > other.size
    
    def __ge__(self, other: 'Directory') -> bool:
        """
        Compares two directories based on their sizes.
        """
        return self.size >= other.size
    
    def __iter__(self):
        """
        Returns an iterator over the contents of the directory.
        """
        return self.__get_content(recursive=self.recursive)
    
    def __next__(self):
        """
        Returns the next item in the directory.
        """
        return next(self.__get_content(recursive=self.recursive))
    
    def __len__(self) -> int:
        """
        Returns the number of items in the directory.
        """
        return self.path.stat().st_nlink
    
    def __contains__(self, item: Union[File, 'Directory']) -> bool:
        """
        Checks if an item is in the directory.
        """
        # Check if item is in the current directory
        if item in os.listdir(self.path):
            return True
        
        # If recursive is True, check subdirectories
        if self.recursive:
            for root, dirs, files in os.walk(self.path):
                if item in files or item in dirs:
                    return True
        return False
    
    def __getitem__(self, search: str) -> Union[File, 'Directory']:
        """
        Gets an item from the directory by name or hash.
        """
        for item in self.__get_content(recursive=self.recursive):
            if item.name == search or hash(item) == search:
                return item
        raise KeyError(f"No item {search} in the directory {self.path}")
    
    def __setitem__(self, search: str, new_item: Union[File, 'Directory']):
        """
        Replaces an item in the directory.
        """
        for item in self.__get_content(recursive=self.recursive):
            if item.name == search or hash(item) == search:
                item.path.rename(new_item.path)
                return
        raise KeyError(f"No item {search} in the directory {self.path}")
    
    def __delitem__(self, search: str):
        """
        Deletes an item from the directory.
        """
        for item in self.__get_content(recursive=self.recursive):
            if item.name == search or hash(item) == search:
                # Check if the item is a file or a directory
                if item.path.is_dir():
                    # Delete the directory recursively
                    shutil.rmtree(item.path)
                else:
                    # Delete the file
                    item.path.unlink()
                return
        raise KeyError(f"No item {search} in the directory {self.path}")
    
    def __pow__(self, other: 'Directory') -> 'Directory':
        """
        Merges two directories.
        Moves all files and subdirectories from the other directory to the current directory, then deletes the other directory.
        """
        for item in other:
            item.path.rename(self.path / item.name)
        other.path.rmdir()
        return self
    
    def __mod__(self, other: str) -> 'Directory':
        """
        Creates a subdirectory in the directory.
        """
        new_dir = self.path / other
        new_dir.mkdir()
        return Directory(new_dir)
    
    def __and__(self, other: 'Directory') -> set:
        """
        Creates a set intersection of two directories contents.
        """
        return set(self.__get_content(recursive=self.recursive)) & set(other.__get_content(other.recursive))
    
    def __or__(self, other: 'Directory') -> 'Directory':
        """
        Combines two directories.
        A set union of two sets is the set of elements that are in either of the sets.
        """
        return set(self) | set(other)
    
    def __invert__(self) -> 'Directory':
        """
        Inverts the directory contents.
        A set difference of two sets is the set of elements that are in the first set, but not in the second set.
        """
        return set(self) ^ set(self)



    # Private methods

    def __human_readable_size(self) -> str:
        """
        Converts the directory size into a human-readable format.
        """
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} EB"

    def __formatted_modification_time(self) -> str:
        """
        Formats the modification time into a human-readable string.
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.modification_time))

    def __get_content(self, recursive: bool = True) -> Iterator[Union[File, 'Directory']]:
        """
        Generator that yields File and Directory instances for the contents of the directory.

        :param recursive: If True, recursively includes contents of subdirectories.
        :return: An iterator over File and Directory instances.
        """
        if recursive:
            items_iterator = self.path.rglob('*')
        else:
            items_iterator = self.path.iterdir()

        for item_path in items_iterator:
            if item_path.is_file():
                try:
                    yield File(item_path)
                except (FileNotFoundError, ValueError) as e:
                    print(f"Error processing file {item_path}: {e}")
            elif item_path.is_dir():
                try:
                    yield Directory(item_path)
                except (FileNotFoundError, ValueError) as e:
                    print(f"Error processing directory {item_path}: {e}")

    def __get_directories(self, recursive: bool = True) -> Iterator['Directory']:
        """
        Generator that yields Directory instances for all subdirectories in the directory.

        :param recursive: If True, recursively includes subdirectories of subdirectories.
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

    def __get_type(self) -> FileType:
        """
        Gets the type of the directory based on its contents.
        """
        file_types = Counter([file.file_type for file in self.__get_files()])
        if file_types:
            return max(file_types, key=file_types.get)
        return FileType.OTHER

    # Public methods
    
    def reload(self):
        """
        Reloads the directory attributes.
        """
        try:
            self.__post_init()
        except Exception as e:
            print(f"Error reloading directory: {e}")

