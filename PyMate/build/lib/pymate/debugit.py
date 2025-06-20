#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import functools
from termcolor import colored

class DebugIt:
    """
    A class-based decorator to print debug information about a function call. 
    """
    
    def __init__(self):
        """Initialize the decorator."""
        pass
    
    def __get__(self, instance, owner):
        """Handle method binding for instance methods."""
        return functools.partial(self.__call__, instance)
    
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(colored(f"DebugIt : {func.__name__}({args}, kwargs={kwargs}) -> {result}", 'yellow'))
            return result
        return wrapper

# Main function to test the decorator
if __name__ == '__main__':
    
    @DebugIt()
    def add(a, b):
        return a + b

    # Test
    add(3, 5)