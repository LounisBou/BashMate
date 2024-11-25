#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import sys

class Infos:
    
    """
    Get information about the application.
    """
    
    @staticmethod
    def get_script_name() -> str:
        """
        Get the name of the executed script.
        """
        return Path(sys.argv[0]).name
    
    @staticmethod
    def get_script_package_name() -> str:
        """
        Get the name of the package of the executed script.
        """
        return Path(sys.argv[0]).parent.resolve().name
    
    @staticmethod
    def get_script_path() -> str:
        """
        Get the path of the executed script.
        """
        return Path(sys.argv[0]).resolve()
    
    @staticmethod
    def get_script_package_path() -> str:
        """
        Get the path of the package of the executed script.
        """
        return Path(sys.argv[0]).parent.resolve()
    
    @staticmethod
    def get_python_version() -> str:
        """
        Get the Python version.
        """
        return sys.version
    
    @staticmethod
    def get_python_executable() -> str:
        """
        Get the Python executable.
        """
        return sys.executable
    
    @staticmethod
    def get_python_path() -> str:
        """
        Get the Python path.
        """
        return sys.path
    
    @staticmethod
    def get_script_args() -> str:
        """
        Get the script arguments.
        """
        return sys.argv[1:]
    
    @staticmethod
    def get_script_pid() -> str:
        """
        Get the script process id.
        """
        return os.getpid()
    
# Main function to test the decorator
if __name__ == '__main__':
    
    # Test the get_script_name function
    print(f"Script name: {Infos.get_script_name()}")
    
    # Test the get_script_package_name function
    print(f"Script package name: {Infos.get_script_package_name()}")
    
    # Test the get_script_path function
    print(f"Script path: {Infos.get_script_path()}")
    
    # Test the get_script_package_path function
    print(f"Script package path: {Infos.get_script_package_path()}")
    
    # Test the get_python_version function
    print(f"Python version: {Infos.get_python_version()}")
    
    # Test the get_python_executable function
    print(f"Python executable: {Infos.get_python_executable()}")
    
    # Test the get_python_path function
    print(f"Python path: {Infos.get_python_path()}")
    
    # Test the get_script_args function
    print(f"Script arguments: {Infos.get_script_args()}")
    
    # Test the get_script_pid function
    print(f"Script PID: {Infos.get_script_pid()}")