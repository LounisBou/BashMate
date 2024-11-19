#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from .file_system_node import FileSystemNode
from .directory import Directory

class FileSystemNodeTree():
    
    """
    A class to hierarchical tree of file system nodes.
    """
    
    # Attributes & initialization
    
    root_node: FileSystemNode = field(init=True, metadata={"help": "The root node to sort."})
    tree: dict = field(init=False, default_factory=dict, metadata={"help": "The tree of file system nodes."})
    
    def __post_init__(self) -> None:
        """
        Initializes the file system node tree.
        """
        # Check if the root node is a directory
        if not self.root_node._is(Directory):
            raise ValueError(f"The root node {self.root_node} is not a directory.")
        # Build tree
        self.tree = self.build_tree(self.root_node)
    
    # Private methods
    
    # Public methods