#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os
import psutil
import functools
from pymate.convertit import ConvertIt

class MemIt:
    
    """
    A decorator class to calculate the memory usage of a function.
    """
    
    def __init__(self, func):
        functools.update_wrapper(self, func)  # Preserve metadata of the decorated function
        self.func = func
        
    def __call__(self, *args, **kwargs):

        # Get the process ID
        pid = os.getpid()
        
        # Get the process
        process = psutil.Process(pid)
        
        # Get the memory usage before the function call
        memory_before = process.memory_info().rss
        
        # Call the function
        result = self.func(*args, **kwargs)
        
        # Get the memory usage after the function call
        memory_after = process.memory_info().rss
        
        # Calculate the memory usage
        memory_used = memory_after - memory_before
        
        # Print the memory usage
        print(f"Memory usage: {ConvertIt.size_human_readable(memory_used)}")
        
        return result
            
# Main function to test the decorator
if __name__ == '__main__':
    
    @MemIt
    def test_function():
        return [i for i in range(1000000)]
    
    test_function()