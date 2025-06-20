#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os
import shutil
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Union

from filemate.file import File
from filemate.file_system_node import FileSystemNode
from filemate.file_type import FileType
from filemate.file_type_extensions import FileTypeExtensions


@dataclass
class Directory(FileSystemNode):

    """ A class to represent a directory. """

    # Attributes specific to the directory

    year: int|None = field(init=False, default=0, metadata="The year in the directory name.")
    recursive: bool = field(init=False, default=False, metadata="If True, includes contents of subdirectories.")

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
        self.stem = self.name.split(' (', maxsplit=1)[0]
        # Year is the year in parentheses if it exists at the end of the name and is a 4-digit number else 0
        self.year = self.name_cleaner.get_year_from_node_name(self.name)
    
    # - String representation
    
    def __str__(self) -> str:
        """
        Returns a string representation of the directory.
        Examples: str(dir) returns a string representation of the directory.
        :return: A string representation of the directory.
        """
        return f"Directory: {self.path.name}"
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the directory.
        Examples: repr(dir) returns a string representation of the directory.
        :return: A string representation of the directory.
        """
        return (f"Directory: {self.path}\n"
                f"Name: {self.name}\n"
                f"Name Cleaned: {self.name_cleaned}\n"
                f"Stem: {self.stem}\n"
                f"Stem Cleaned: {self.stem_cleaned}\n"
                f"Year: {self.year}\n"
                f"Size: {self.human_readable_size()}\n"
                f"Items: {self.count()}\n"
                f"  - Files: {self.count_files()}\n"
                f"  - Subdirectories: {self.count_dirs()}\n"
                f"Recursive: {self.recursive}\n"
                f"Last Modified: {self.formatted_modification_time()}\n"
                f"Type: {self.get_type()}")

    # - Iteration and containment
    
    def __iter__(self) -> Iterator[FileSystemNode]:
        """
        Returns an iterator over the contents of the directory.
        Example: iter(dir) returns an iterator over the nodes of the directory.
        """
        return self.iter(recursive=self.recursive)
    
    def __next__(self) -> FileSystemNode:
        """
        Returns the next node in the directory.
        Example: next(dir) returns the next node in the directory.
        """
        return next(self.iter(recursive=self.recursive))
    
    def __contains__(self, node: FileSystemNode) -> bool:
        """
        Checks if a node is in the directory.
        Example: file in dir checks if the file is in the directory.
        :param node: The node to check.
        :return: True if the node is in the directory, False otherwise.
        """
        # Get the target name
        target_name = node.path.name

        # Check if item is in the current directory
        with os.scandir(self.path) as entries:
            for entry in entries:
                if entry.name == target_name:
                    return True

        # If recursive is True, check subdirectories
        if getattr(self, 'recursive', False):  # Check if the `recursive` attribute exists and is True
            for _, dirs, files in os.walk(self.path):
                if target_name in files or target_name in dirs:
                    return True

        return False
    
    def __getitem__(self, search: str) -> FileSystemNode:
        """
        Gets an item from the directory by name or hash.
        Example: dir['file.txt'] gets the file 'file.txt' from the directory.
        :param search: The name or hash of the item to get.
        :return: The node in the directory.
        """
        for node in self.iter(recursive=self.recursive):
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
        for node in self.iter(recursive=self.recursive):
            if node.name == search or hash(node) == search:
                node.move(new_node.path)
                return
        raise KeyError(f"No node {search} in the directory {self.path}")
    
    def __delitem__(self, search: str) -> None:
        """
        Deletes an node from the directory.
        Example: del dir['file.txt'] deletes the file 'file.txt' from the directory.
        :param search: The name or hash of the node to delete.
        """
        for node in self.iter(recursive=self.recursive):
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
    
    def __truediv__(self, other: Union[str, Path, FileSystemNode]) -> FileSystemNode:
        """
        Concatenates the directory path with a string, path, or node.
        example: dir / 'file.txt' returns a file named 'file.txt' in the directory.
        :param other: The string, path, or node to concatenate.
        :return: A FileSystemNode instance for the concatenated path.
        """
        
        if isinstance(other, str):
            path = self.path / other
        elif isinstance(other, Path):
            path = self.path / other
        elif isinstance(other, Directory):
            path = self.path / other.name
        elif isinstance(other, File):
            path = self.path / other.name
        else:
            raise TypeError(f"Unsupported type {type(other)} for concatenation.")
        if path.is_dir():
            return Directory(path)
        elif path.is_file():
            return File(path)
    
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
        return set(self.iter(recursive=self.recursive)) & set(other.iter(other.recursive))
    
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

    # Public methods

    def iter(self, recursive: bool = False, hidden: bool = False) -> Iterator[FileSystemNode]:
        """
        Generator that yields FileSystemNode instances for the contents of the directory.

        :param recursive: If True, recursively includes contents of subdirectories.
        :param hidden: If True, includes hidden files and directories.
        :yield: An iterator over FileSystemNode instances.
        """
        try:
            # Use appropriate iterator based on recursive flag
            nodes_iterator = self.path.rglob('*') if recursive else self.path.iterdir()

            for node_path in nodes_iterator:
                # Skip hidden files/directories unless `hidden` is True
                if not hidden and node_path.name.startswith('.'):
                    continue

                # Use FileSystemNodeFactory to dynamically create nodes
                try:
                    if node_path.is_file():
                        yield File(node_path)
                    elif node_path.is_dir():
                        yield Directory(node_path)
                except (FileNotFoundError, ValueError) as e:
                    raise ValueError(f"Error processing {node_path}: {e}") from e

        except Exception as e:
            raise RuntimeError(f"Error accessing contents of {self.path}: {e}") from e


    def iter_dir(self, recursive: bool = False, hidden: bool = False) -> Iterator['Directory']:
        """
        Generator that yields Directory instances for all subdirectories in the directory.

        :param recursive: If True, recursively includes subdirectories of subdirectories.
        :param hidden: If True, includes hidden directories.
        :yield: An iterator over Directory instances.
        """
        for node in self.iter(recursive=recursive, hidden=hidden):
            if node.is_instance(Directory):
                yield node
    
    def iter_files(self, recursive: bool = False, hidden: bool = False) -> Iterator[File]:
        """
        Generator that yields File instances for all files in the directory.

        :param recursive: If True, recursively includes files in subdirectories.
        :param hidden: If True, includes hidden files.
        :yield: An iterator over File instances.
        """
        for node in self.iter(recursive=recursive, hidden=hidden):
            if node.is_instance(File):
                yield node
    
    def get_size(self) -> int:
        """
        Gets the total size of the directory in bytes by us
        :return: The total size of the directory in bytes.
        """
        if self.size is None:
            self.size = sum(file.get_size() for file in self.iter_files())
        return self.size
    
    def get_type(self) -> FileType:
        """
        Gets the type of the directory based on its contents.
        :return: The FileType of the directory
        """
        files = list(self.iter_files(recursive=True))
        # Remove files with no extension or with extensions to ignored
        extension_to_ignore = [None, '', '.DS_Store'] + FileTypeExtensions.OTHER.value + FileTypeExtensions.IMAGE.value + FileTypeExtensions.DOCUMENT.value
        files_to_ignore = [file for file in files if file.extension in extension_to_ignore]
        files = [file for file in files if file not in files_to_ignore]
        file_types = Counter([file.get_type() for file in files])
        if file_types:
            return max(file_types, key=file_types.get)
        return FileType.OTHER
        
    def count(self) -> int:
        """
        Returns the number of nodes in the directory.
        :return: The number of nodes in the directory.
        """
        return sum(1 for _ in self.iter(recursive=False))
    
    def count_dirs(self) -> int:
        """
        Returns the number of subdirectories in the directory.
        :return: The number of subdirectories in the directory.
        """
        return sum(1 for _ in self.iter_dir(recursive=False))
    
    def count_files(self) -> int:
        """
        Returns the number of files in the directory.
        :return: The number of files in the directory.
        """
        return sum(1 for _ in self.iter_files(recursive=False))
    
    def delete(self, recursive = False) -> None:
        """
        Delete the directory.
        :param recursive: If True, removes the directory and its contents.
        """
        if recursive is True:
            shutil.rmtree(self.path)
        else:
            self.path.rmdir()
    
    def unpack(self, clean: bool = False, file_only: bool = False, dir_only: bool = False) -> set[FileSystemNode]:
        """
        Unpacks the contents of the directory.
        Moves all files and subdirectories from the directory to its parent directory.
        :param clean: If True, cleans the nodes names before moving them.
        :param file_only: If True, only moves files and not subdirectories.
        :param dir_only: If True, only moves subdirectories and not files.
        :return: A set of the nodes that were unpacked.
        """
        unpacked = set[FileSystemNode]()
        for node in self:
            if file_only and node.is_instance(Directory):
                continue
            if dir_only and node.is_instance(File):
                continue
            if clean:
                node.clean_name()
            # Move the node to the parent directory
            node.move(self.path.parent / node.name)
            unpacked.add(node)
        # Remove the directory if it is empty
        if not os.listdir(self.path):
            self.delete()
        return unpacked