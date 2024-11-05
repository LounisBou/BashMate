#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import re
from .file_system_node import FileSystemNode
from .file_type import FileType
from .file_type_extensions import FileTypeExtensions
from .file_cleaner import FileCleaner

@dataclass
class File(FileSystemNode):
    
    """A class to represent a file."""

    # Attributes specific to files
    extension: str = None

    # Special methods
    
    # - Initialization and deletion

    def __post_init__(self) -> None:
        """
        Initializes the file attributes.
        """
        # Superclass initialization
        super().__post_init__()
        # Ensure node is a file
        if not self.path.is_file():
            raise ValueError(f"The path {self.path} is not a file.")
        # Set the file attributes
        self.name_cleaned = FileCleaner.get_cleaned_file_name(self.path)
        self.stem = self.path.stem
        self.stem_cleaned = FileCleaner.get_cleaned_file_stem(self.path)
        self.extension = self.path.suffix[1:].lower()  # Remove leading dot and convert to lowercase
        self.size = self.path.stat().st_size / (1024 * 1024) # Convert size to MB
        self.modification_time = self.path.stat().st_mtime

    def __del__(self) -> None:
        """
        Frees the resources used by the file.
        Example: del file
        """
        super().__del__()
        del self.extension

    # - String representation

    def __str__(self) -> str:
        """
        Returns a string representation of the file.
        Example: str(file)
        :return: A string representation of the file.
        """
        return (f"File: {self.path}\n"
                f"Name: {self.name}\n"
                f"Extension: {self.extension}\n"
                f"Size: {self.human_readable_size()}\n"
                f"Last Modified: {self.formatted_modification_time()}\n"
                f"Type: {self.get_type()}")
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the file.
        Example: repr(file)
        :return: A string representation of the file.
        """
        return f"File({self.path!r})"
    
    # - Comparison

    def __contains__(self, item: str) -> bool:
        """
        Checks if a string is contained in the file name.
        Example: 'string' in file
        :param item: The string to search for.
        :return: True if the string is contained in the file name, False otherwise.
        """
        return item in self.stem
    
    # Private methods

    # Public methods
    
    def get_type(self) -> FileType:
        """
        Gets the type of a file based on its extension.
        :param filepath: Path of the file.
        :return: The type of the file.
        """

        # Get the file type based on the extension
        file_type = FileTypeExtensions.get_file_type(self.extension)
        
        # Check if the file type is None
        if file_type is None:
            return FileType.OTHER.name
        
        # Override the file type for specific cases
        if file_type.name == FileTypeExtensions.VIDEO.name:
            if re.search(r's\d{2}e\d{2}', self.name) or re.search(r'\d{3,4}p', self.name):
                file_type = FileType.TVSHOW
            else:
                file_type = FileType.MOVIE
            
        # Return the file type
        return file_type.name
    
