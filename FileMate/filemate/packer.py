#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
from dataclasses import dataclass, field
from filemate.file_system_node_tree import FileSystemNodeTree


@dataclass
class Packer:
    
    source: FileSystemNodeTree 