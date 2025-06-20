#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from bigtree import Node as TreeNode
from bigtree import dict_to_tree, print_tree, tree_to_dict
from pymate import CacheIt, LogIt, SaveIt, TimeIt
from termcolor import colored

from filemate.directory import Directory
from filemate.file_system_node import FileSystemNode


@dataclass
class FileSystemNodeTree():
    
    """
    A class to hierarchical tree of file system nodes.
    """
    
    # Attributes & initialization
    
    nodetree_folder_name: ClassVar[str] = "__nodetree__"
    redis_config: ClassVar[dict] = {"host": "localhost", "port": 6379, "db": 0}
    
    root_node: FileSystemNode = field(init=True, metadata={"help": "The root node to sort."})
    verbose: bool = field(init=True, default=False, metadata={"help": "Verbose output."})
    root_tree_node: TreeNode = field(init=False, default=None, metadata={"help": "The root tree node."})
    logger: LogIt = field(init=True, default_factory=LogIt, metadata={"help": "The logger."})
    saveit: SaveIt = field(init=False, default_factory=SaveIt, metadata={"help": "The SaveIt instance."})
    
    def __post_init__(self) -> None:
        """
        Initializes the file system node tree.
        """
        # Check if the root node is a directory
        if not self.root_node.is_instance(Directory):
            raise ValueError(f"The root node {self.root_node} is not a directory.")
        # Create an instance of saveit
        self.saveit = SaveIt(backend='redis', redis_config=FileSystemNodeTree.redis_config)
    
    # Private methods
    
    @TimeIt
    def __build_tree(self) -> None:
        """
        Builds the tree of file system nodes.
        """
        self.root_tree_node = FileSystemNodeTree.create_node(self.root_node)
        self.__build_tree_recursive(self.root_node, self.root_tree_node)
    
    @CacheIt(max_duration=3600, backend='redis', redis_config=redis_config)
    def __build_tree_recursive(self, node: Directory, tree_node: TreeNode) -> None:
        """
        Builds the tree of file system nodes recursively.
        :param node: The file system node.
        :param tree_node: The tree node.
        """
        # Iterate over the node's children
        for child_node in node.iter(recursive=False, hidden=False):
            try:
                # Create tree node
                child_tree_node = FileSystemNodeTree.create_node(child_node, parent=tree_node)
                if child_node.is_instance(Directory):
                    self.__build_tree_recursive(child_node, child_tree_node)
            except (OSError, AttributeError) as e:
                self.logger.info(colored(f"Skipping node {child_node.path.name} due to error: {e}"), "yellow")
                
    def __str__(self) -> str:
        """
        Returns a string representation of the file system node tree.
        :return: A string representation of the file system node tree.
        """
        return f"File System Node Tree: {self.root_node.path}"
        
    # Public methods
    
    # - Build tree
    
    def build(self) -> None:
        """
        Builds the tree of file system nodes.
        """
        self.__build_tree()
    
    # - Add & Remove nodes
    
    def add_node(self, parent_path: Path, child_node: FileSystemNode) -> None:
        """
        Adds a new node to the tree under the specified parent path.
        """
        parent_tree_node = self.search_node_by_path(parent_path)
        if parent_tree_node is None:
            raise ValueError(f"Parent path {parent_path} not found in the tree.")
        FileSystemNodeTree.create_node(child_node, parent=parent_tree_node)

    def remove_node(self, path: Path) -> None:
        """
        Removes a node from the tree by its path.
        """
        node_to_remove = self.search_node_by_path(path)
        if node_to_remove is None:
            raise ValueError(f"Path {path} not found in the tree.")
        node_to_remove.parent = None  # Detach the node from its parent
    
    # - Display
    
    def show(self) -> None:
        """
        Displays the file system tree using bigtree's print_tree function.
        """
        print_tree(self.root_tree_node)
        
    # - Export & Import
    
    def tree_to_dict(self) -> dict:
        """
        Converts the tree structure into a dictionary.
        :return: Dictionary representation of the tree.
        """
        return tree_to_dict(self.root_tree_node)
       
    @staticmethod
    def dict_to_tree(data: dict) -> TreeNode:
        """
        Recursively converts a dictionary into a TreeNode.
        :param data: Dictionary representation of the node.
        :return: The TreeNode instance.
        """
        return dict_to_tree(data)

    def json(self, indent: int = 4) -> str:
        """
        Transforms the tree to a JSON string.
        :param indent: The number of spaces to indent the JSON string.
        :return: A JSON string representing the hierarchical structure
        """
        return json.dumps(self.tree_to_dict(), indent=indent)
    
    def export(self, file_path: str, indent: int = 4) -> None:
        """
        Exports the tree to a JSON file.
        :param file_path: Path to save the tree.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json_data = self.json(indent=indent)
            f.write(json_data)
    
    @staticmethod
    def importer(file_path: str) -> 'FileSystemNodeTree':
        """
        Imports the tree from a JSON file.
        :param file_path: Path to the JSON file.
        :return: An instance of FileSystemNodeTree.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
        
        return FileSystemNodeTree.dict_to_tree(tree_data)
    
    # - Search methods
    
    def search_node_by_name(self, name: str) -> TreeNode|None:
        """
        Searches for a node in the tree by name.
        
        :param name: Name of the node to search for.
        :return: The matching TreeNode if found, None otherwise.
        """
        # Traverse the tree to find a node by name
        def _find_by_name(node, name):
            if node.name == name:
                return node
            for child in getattr(node, "children", []):
                result = _find_by_name(child, name)
                if result is not None:
                    return result
            return None
        return _find_by_name(self.root_tree_node, name)
    
    def search_node_by_path(self, path: Path) -> TreeNode | None:
        """
        Searches for a node in the tree by its absolute or relative path.

        :param path: Path of the node to search for.
        :return: The matching TreeNode if found, None otherwise.
        """
        
        # Normalize the path and split it into parts
        normalized_path = Path(path).resolve().parts
        current_node = self.root_tree_node

        # Split the path into parts and search hierarchically
        for part in normalized_path:
            current_node = next(
                (child for child in current_node.children if child.name == part),
                None
            )
            if current_node is None:
                return None  # Node not found

        return current_node
    
    # - Utility methods
    
    @TimeIt
    def save(self) -> None:
        """
        Saves the tree to a JSON file in nodetree folder.
        """
        # Check if the nodetree folder exists
        nodetree_folder = Path(FileSystemNodeTree.nodetree_folder_name)
        if not nodetree_folder.exists():
            nodetree_folder.mkdir()
        # Check if the tree has been saved
        if FileSystemNodeTree.check_saved_tree(self.root_node.name):
            # Remove the existing saved tree
            (nodetree_folder / f"{self.root_node.name}.json").unlink()
        # Export the tree to a JSON file
        self.export(f"{FileSystemNodeTree.nodetree_folder_name}/{self.root_node.name}.json")

    @staticmethod
    @TimeIt
    def restore(node_name: str) -> 'FileSystemNodeTree':
        """
        Restores the tree from a JSON file in nodetree folder.
        :param node_name: Name of the node.
        :return: An instance of FileSystemNodeTree.
        """
        # Check if the tree has been saved
        if not FileSystemNodeTree.check_saved_tree(node_name):
            raise FileNotFoundError("No saved tree found.")
        return FileSystemNodeTree.importer(f"{FileSystemNodeTree.nodetree_folder_name}/{node_name}.json")
    
    @staticmethod
    def check_saved_tree(node_name: str, max_age: int|None = None) -> bool:
        """
        Checks if the tree has been saved.
        :param node_name: Name of the node.
        :param max_age: Maximum age in seconds for the saved tree. None to ignore.
        :return: True if the tree has been saved, False otherwise.
        """
        # Check if max_age is set
        if max_age is not None:
            # Check if the saved tree exists and is not older than max_age
            nodetree_path = Path(f"{FileSystemNodeTree.nodetree_folder_name}/{node_name}.json")
            if nodetree_path.exists():
                return (time.time() - nodetree_path.stat().st_mtime) < max_age
            return False
        return Path(f"{FileSystemNodeTree.nodetree_folder_name}/{node_name}.json").exists()
    
    @staticmethod
    def create_node(node: FileSystemNode, parent: TreeNode = None) -> TreeNode:
        """
        Creates a new TreeNode instance.
        :param node: File system node to create a TreeNode from.
        :param parent: Parent TreeNode.
        :return: The created TreeNode
        """
        return TreeNode(
            node.path.name, 
            parent=parent,
            size=node.get_size(),
            type=node.get_type()
        )
    
    def children(self) -> list[TreeNode]:
        """
        Checks if a node is the root of the tree.
        :param node: The node to check.
        :return: True if the node is the root, False otherwise.
        """
        return self.root_tree_node.children
    
    