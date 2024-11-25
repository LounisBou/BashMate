#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os
import psutil
import functools

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
        print(f"Memory usage: {self._human_readable_size(memory_used)}")
        
        return result
    
    def _human_readable_size(self, size):
        """
        Convert the size in bytes to a human-readable format.
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.2f} {unit}"
        
# Main function to test the decorator
if __name__ == '__main__':
    
    @MemIt
    def test_function():
        return [i for i in range(1000000)]
    
    test_function()