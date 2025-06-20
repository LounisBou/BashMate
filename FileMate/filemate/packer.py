#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from pymate import LogIt

from dotenv import load_dotenv
from filemate.file_system_node_tree import FileSystemNodeTree
from filemate.file_system_node import FileSystemNode
from filemate.directory import Directory

@dataclass
class Packer:
    
    """
    Packer class for packing file system nodes from a source tree to a destination tree.
    This class provides methods to pack, override, merge, and replace file system nodes
    between two file system node trees. It supports operations such as overriding existing
    nodes, merging nodes, and replacing nodes in the destination tree with those from the source tree
    """
    
    source: FileSystemNodeTree = field(init=True, default=None, metadata={"help": "The source file system node tree."})
    destination: FileSystemNodeTree = field(init=True, default=None, metadata={"help": "The destination file system node tree."})
    override: bool = field(init=True, default=False, metadata={"help": "Override destination nodes if they exist."})
    merge: bool = field(init=True, default=False, metadata={"help": "Merge the source and destination nodes."})
    verbose: bool = field(init=True, default=False, metadata={"help": "Verbose output."})
    logger: LogIt = field(init=True, default_factory=LogIt, metadata={"help": "The logger."})
    
    def __post_init__(self) -> None:
        """
        Initializes the packer.
        """
        # Load the environment variables
        load_dotenv()
        
        
    def pack_all(self) -> None:
        """
        Packs the entire source file system node tree into the destination file system node tree.
        """
        # For each first level node in the source tree
        for node_from_source in self.source.root_node.children:
            # Find the node_from_source in the destination tree
            node_from_destination = self.destination.search_node_by_name(node_from_source)
            # Pack the node_from_source into the node_from_destination
            self.pack(node_from_source, node_from_destination)
        

    def pack(self, node_from_source: FileSystemNode, node_from_destination: FileSystemNode = None) -> None:
        """
        Packs the source file system node tree into the destination file system node tree.
        :param node_from_source: The source file system node.
        :param node_from_destination: The destination file system node. Default is None.
        :return: bool - True if the packing was successful, False otherwise.
        """
        # Check if node_from_destination is None
        if node_from_destination is None:
            # Find node_from_source in the destination tree
            node_from_destination = self.destination.search_node_by_name(node_from_source)
        # Check if node_from_destination exists
        if node_from_destination is not None:
            # Check if override is True
            if self.override:
                # Override the node_from_destination
                self.override_node(node_from_source, node_from_destination)
            # Check if merge is True
            elif self.merge:
                # Merge the node_from_source and node_from_destination
                self.merge_node(node_from_source, node_from_destination)
            # Check if override and merge are False
            else:
                # Replace the content of node_from_destination with the content of node_from_source
                self.replace_node(node_from_source, node_from_destination)
                
    def override_node(self, node_from_source: FileSystemNode, node_from_destination: FileSystemNode) -> None:
        """
        Overrides the destination file system node with the source file system node.
        :param node_from_source: The source file system node.
        :param node_from_destination: The destination file system node.
        """
        # Check if node_from_source is a directory
        if node_from_source.is_instance(Directory):
            # Check if node_from_destination is a directory
            if node_from_destination.is_instance(Directory):
                # Override the directory
                self.override_directory(node_from_source, node_from_destination)
            else:
                # Replace the content of node_from_destination with the content of node_from_source
                self.replace_node(node_from_source, node_from_destination)
        else:
            # Replace the content of node_from_destination with the content of node_from_source
            self.replace_node(node_from_source, node_from_destination)
            
    def override_directory(self, node_from_source: Directory, node_from_destination: Directory) -> None:
        """
        Overrides the destination directory with the source directory.
        :param node_from_source: The source directory.
        :param node_from_destination: The destination directory.
        """
        # Iterate over the source directory's children
        for child_node_from_source in node_from_source.iter(recursive=False, hidden=False):
            # Find the child_node_from_source in the destination directory
            child_node_from_destination = self.destination.search_node_by_name(child_node_from_source)
            # Check if child_node_from_destination exists
            if child_node_from_destination is not None:
                # Pack the child_node_from_source into the child_node_from_destination
                self.pack(child_node_from_source, child_node_from_destination)
            else:
                # Add the child_node_from_source to the destination directory
                self.add_node(child_node_from_source, node_from_destination)
                
    def merge_node(self, node_from_source: FileSystemNode, node_from_destination: FileSystemNode) -> None:
        """
        Merges the source file system node with the destination file system node.
        :param node_from_source: The source file system node.
        :param node_from_destination: The destination file system node.
        """
        # Check if node_from_source is a directory
        if node_from_source.is_instance(Directory):
            # Check if node_from_destination is a directory
            if node_from_destination.is_instance(Directory):
                # Merge the directory
                self.merge_directory(node_from_source, node_from_destination)
            else:
                # Replace the content of node_from_destination with the content of node_from_source
                self.replace_node(node_from_source, node_from_destination)
        else:
            # Replace the content of node_from_destination with the content of node_from_source
            self.replace_node(node_from_source, node_from_destination)
            
    def merge_directory(self, node_from_source: Directory, node_from_destination: Directory) -> None:
        """
        Merges the source directory with the destination directory.
        :param node_from_source: The source directory.
        :param node_from_destination: The destination directory.
        """
        # Iterate over the source directory's children
        for child_node_from_source in node_from_source.iter(recursive=False, hidden=False):
            # Find the child_node_from_source in the destination directory
            child_node_from_destination = self.destination.search_node_by_name(child_node_from_source)
            # Check if child_node_from_destination exists
            if child_node_from_destination is not None:
                # Merge the child_node_from_source into the child_node_from_destination
                self.merge_node(child_node_from_source, child_node_from_destination)
            else:
                # Add the child_node_from_source to the destination directory
                self.add_node(child_node_from_source, node_from_destination)
                
    def replace_node(self, node_from_source: FileSystemNode, node_from_destination: FileSystemNode) -> None:
        """
        Replaces the content of the destination file system node with the content of the source file system node.
        :param node_from_source: The source file system node.
        :param node_from_destination: The destination file system node.
        """
        # Check if node_from_source is a directory
        if node_from_source.is_instance(Directory):
            # Check if node_from_destination is a directory
            if node_from_destination.is_instance(Directory):
                # Replace the directory
                self.replace_directory(node_from_source, node_from_destination)
            else:
                # Replace the content of node_from_destination with the content of node_from_source
                self.add_node(node_from_source, node_from_destination.parent)
        else:
            # Replace the content of node_from_destination with the content of node_from_source
            self.add_node(node_from_source, node_from_destination.parent)
        
    def replace_directory(self, node_from_source: Directory, node_from_destination: Directory) -> None:
        """
        Replaces the content of the destination directory with the content of the source directory.
        :param node_from_source: The source directory.
        :param node_from_destination: The destination directory.
        """
        # Remove the destination directory
        self.remove_node(node_from_destination)
        # Add the source directory to the destination directory's parent
        self.add_node(node_from_source, node_from_destination.parent)
        
    def add_node(self, node: FileSystemNode, parent: FileSystemNode) -> None:
        """
        Adds a new node to the parent node.
        :param node: The new node to add.
        :param parent: The parent node.
        """
        # Add the node to the parent
        self.destination.add_node(parent.path, node)
        
    def remove_node(self, node: FileSystemNode) -> None:
        """
        Removes a node from the destination tree.
        :param node: The node to remove.
        """
        # Remove the node from the destination tree
        self.destination.remove_node(node.path)
        
    def __str__(self) -> str:
        """
        Returns a string representation of the packer.
        :return: A string representation of the packer.
        """
        return f"Packer: Source={self.source.root_node.path}, Destination={self.destination.root_node.path}"
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the packer.
        :return: A string representation of the packer.
        """
        return f"Packer: Source={self.source.root_node.path}, Destination={self.destination.root_node.path}"
    
    def __bool__(self) -> bool:
        """
        Returns True if the packer is valid, False otherwise.
        :return: bool - True if the packer is valid, False otherwise.
        """
        return self.source is not None and self.destination is not None
    
    def __call__(self, node_from_source: FileSystemNode, node_from_destination: FileSystemNode = None) -> None:
        """
        Packs the source file system node tree into the destination file system node tree.
        :param node_from_source: The source file system node.
        :param node_from_destination: The destination file system node. Default is None.
        """
        self.pack(node_from_source, node_from_destination)
        