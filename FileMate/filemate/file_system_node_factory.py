#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from pathlib import Path
from filemate.file_system_node import FileSystemNode
from filemate.directory import Directory
from filemate.file import File

class FileSystemNodeFactory():
    
    """
    A class to create file system nodes.
    """
    
    @classmethod
    def create_node(cls, path: Path) -> FileSystemNode:
        """
        Creates a file system node based on the type of the path.
        :param path: Path of the file system node.
        :return: A file system node.
        """
        if path.is_file():
            return File(path)
        elif path.is_dir():
            return Directory(path)
        else:
            raise ValueError(f"The path {path} is not a file or directory.")
    
        