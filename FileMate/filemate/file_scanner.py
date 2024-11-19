#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from .file_system_node import FileSystemNode

class FileScanner():
    
    """
    A class to scan files and directories from a file system node, generating a tree structure.
    """
    
    # Attributes & initialization
    
    root_node: FileSystemNode = field(init=True, metadata={"help": "The root node to sort."})
    
    def __post_init__(self) -> None:
        """
        Initializes the file sorter attributes.
        """
        # Superclass initialization
        super().__post_init__()