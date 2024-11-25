#!/usr/bin/env python 
# -*- coding: utf-8 -*-

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
        return Path(sys.argv[0]).stem
    
    @staticmethod
    def get_script_package_name() -> str:
        """
        Get the name of the package of the executed script.
        """
        return Path(sys.argv[0]).parent.resolve().name
    
    
# Main function to test the decorator
if __name__ == '__main__':
    
    # Test the get_script_name function
    print(Infos.get_script_name())