#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import re
import shutil
import sys
import os
from pathlib import Path
from typing import List
from .file_type import FileType
from .file_cleaner import FileCleaner
from .directory import Directory

class FileSorter:
    """
    A class to sort files corresponding directories based on their filename and extension.
    The class can clean filenames, pack files into directories, and sort them accordingly.
    """

    # DEBUG
    DEBUG = True
    
    # Directories by file type
    SORTED_DIR = {
        FileType.MOVIE: "001-MOVIES",
        FileType.TVSHOW: "002-TVSHOWS",
        FileType.EBOOK: "003-EBOOKS",
        FileType.AUDIO: "004-AUDIO",
        FileType.APP: "005-APPS",
        FileType.ANDROID: "006-ANDROID",
        FileType.SCRIPT: "099-SCRIPTS",
        'unpacked': "100-UNPACKED",
    }

    # Allowed file types for directory sorting
    ALLOWED_TYPES = {
        FileType.MOVIE: [FileType.MOVIE, FileType.SUBTITLE],
        FileType.TVSHOW: [FileType.TVSHOW, FileType.MOVIE, FileType.SUBTITLE],
        FileType.EBOOK: [FileType.EBOOK],
        FileType.AUDIO: [FileType.AUDIO],
        FileType.APP: [FileType.APP],
        FileType.IMAGE: [FileType.IMAGE],
        FileType.ISO: [FileType.ISO],
        FileType.ANDROID: [FileType.ANDROID],
        FileType.SCRIPT: [FileType.SCRIPT],
    }
    
    # Public methods
    
    @staticmethod
    def is_sorted_dir(path: Path) -> bool:
        """
        Determines if a directory is a sorted directory.

        :param path: The path of the directory to check.
        :return: True if the directory is a sorted directory, False otherwise.
        """
        # Check if it is a directory
        if not path.is_dir():
            return False
        # Check if the directory is in the sorted directories list
        in_sorted_list = path.name in FileSorter.SORTED_DIR.values()
        # Check if the directory match the sorted directories pattern (XXX-NAME) or (XXX NAME) with XXX being a number
        match_sorted_pattern = re.match(r"^\d{3}[- ]\w+$", path.name) is not None
        # Return True if the directory is in the sorted directories list or match the sorted directories pattern
        return in_sorted_list or match_sorted_pattern
   
    @staticmethod
    def get_dir_files_type(path: Path) -> FileType:
        """
        Gets the type of a directory based on its content.

        :param path: The full path of the directory.
        :return: The file type of the directory.
        """

        # Sorted directory are type OTHER
        if not FileSorter.is_sorted_dir(path):        
            # Check every types
            for file_type in FileType.types():
                # Check if the directory contains files of the current type
                if any([FileType.match(file_type, path.joinpath(filename)) for filename in path.iterdir()]):
                    return file_type
        
        return FileType.OTHER

    @staticmethod
    def pack(path: Path) -> Path|None:
        """
        Packs a media file into a directory named after the cleaned basename.

        :param path: The full path of the file to pack.
        :return: The path of the packed directory or None if the file could not be packed.
        """
        if path.is_file():
            # Target directory path is cleaned basename of the file in the same directory
            cleaned_file_stem = FileCleaner.get_cleaned_file_stem(path)
            target_dir = path.parent.joinpath(cleaned_file_stem)
            # Create the target directory if it does not exist
            os.makedirs(target_dir, exist_ok=True)
            # Move the file into the target directory
            shutil.move(path, target_dir)
            return target_dir
        return None

    @staticmethod
    def unpack(source_path: Path, target_path: Path) -> List[Path]:
        """
        Unpacks all files from a directory into the parent directory.

        :param source_path: The path of the directory to unpack.
        :param target_path: The path of the directory to unpack to.
        :return: A list of the paths of the unpacked files.
        """

        # Check if the directory is a sorted directory
        if FileSorter.is_sorted_dir(source_path):
            return []
        
        # Unpack the directory
        if source_path.is_dir():
            unpacked_filepaths = []
            for element in source_path.iterdir():
                filepath = source_path.joinpath(element)
                # Check if the element is a file
                if filepath.is_file():
                    shutil.move(filepath, target_path)
                    unpacked_filepath = target_path.joinpath(filepath.name)
                    unpacked_filepaths.append(unpacked_filepath)
                elif filepath.is_dir():
                    # Unpack the subdirectory
                    unpacked_filepaths.extend(FileSorter.unpack(filepath, target_path))
            # Remove the empty directory
            try:
                source_path.rmdir()
            except OSError:
                print(f"Could not remove directory: {source_path}, directory is not empty.")
            return unpacked_filepaths
        return []
    
    """ Process methods """

    @staticmethod
    def sort(path: Path) -> None:
        """
        Sorts file into either the corresponding file type directory.

        :param path: The path of the file/directory to sort.
        :return: None
        """
        
        # Is directory
        if path.is_dir():
            type = FileSorter.get_dir_files_type(path)
        else:
            type = FileType.get(path)

        # Check if the file type is not allowed
        if type == FileType.OTHER:
            return
        
        # Unpack the directory if it is a sorted directory
        if path.is_dir():
            # Depack the directory
            filepaths = FileSorter.unpack(path)
        else:
            filepaths = [path]
        
        # Determine the sorted directory path
        sorted_dir = path.parent.joinpath(FileSorter.SORTED_DIR[type])
        # Process each file
        for filepath in filepaths:
            # Determine if the file is an allowed type
            if FileType.get(filepath) in FileSorter.ALLOWED_TYPES[type]:
                # Determine the cleaned file stem
                cleaned_file_stem = FileCleaner.get_cleaned_file_stem(filepath)
                # DEBUG
                print(f"Cleaned file stem: {cleaned_file_stem}")
                # Determine the target path
                target_path = sorted_dir.joinpath(cleaned_file_stem)
                # Create the directory if it does not exist
                target_path.mkdir(parents=True, exist_ok=True)
                # Move the file into the target directory withtout renaming it
                shutil.move(filepath, target_path)
            else:
                # Delete the file if it is not a media file or a subtitle
                filepath.unlink()

    @staticmethod
    def process(directory: Directory) -> None:
        """
        Processes all directories and files in the 'ToSort' directory. Unpacks, packs, and sorts media files.

        :param path: The path of the directory to process.
        :return: None
        """

        # DEGUG
        print(f"Processing directory: {path}")

        # Process all elements in the directory
        for element in path.iterdir():
            # Check if element is a directory
            element_path = path.joinpath(element)
            # Do not process sorted directories
            if FileSorter.is_sorted_dir(element_path):
                continue
            # Do not process hidden files
            if element.name.startswith('.'):
                continue
            # DEBUG
            print(f"Sorting: {element_path}")
            # Process the element
            FileSorter.sort(element_path)

### Main program ###
if __name__ == "__main__":
    # Check first command-line argument to see if it is a directory
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if path.is_dir():
            FileSorter.process(path)
        else:
            print("The provided path is not a valid directory.")
            sys.exit(1)
    else:
        print("Please provide a directory path as an argument.")
        sys.exit(1)