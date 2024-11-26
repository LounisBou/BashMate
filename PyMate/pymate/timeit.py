#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import time
import functools

class TimeIt:
    """
    A class-based decorator to measure the execution time of a function.
    """
    def __init__(self, func: callable):
        """Initialize the decorator with the given function."""
        functools.update_wrapper(self, func)  # Preserve metadata of the decorated function
        self.func = func

    def __get__(self, instance, owner):
        """Handle method binding for instance methods."""
        return functools.partial(self.__call__, instance)

    def __call__(self, *args, **kwargs):
        """Call the decorated function and measure its execution time."""
        start_time = time.perf_counter()
        result = self.func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {self.func.__name__}{args} Took {total_time:.4f} seconds')
        return result
    
# Main function to test the decorator
if __name__ == '__main__':
    
    @TimeIt
    def test_function(n):
        return sum(range(n))

    test_function(1000000)
    test_function(10000000)
    test_function(100000000)
