#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from diskcache import Cache

class CacheIt:
    """
    A caching decorator for persistent on-disk caching across an entire project.
    """
    cache = Cache('__cacheit__')
    
    def __init__(self, max_duration=3600):
        """
        Initialize the cache parameters.
        Arguments:
            max_size (int): Maximum cache size in bytes. 0 means no limit.
            max_duration (int): Cache duration in seconds.
            cache_dir (str): Directory to store the shared on-disk cache.
        """
        self.max_duration = max_duration

    def __call__(self, func):
        
        # Preserve metadata of the decorated function
        functools.update_wrapper(self, func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a unique cache key
            key = (func.__name__, args, frozenset(kwargs.items()))

            # Check if the key exists in the cache
            if key in self.cache:
                print(f"Cache hit for {func.__name__}{args}")
                result = self.cache[key]
            else:
                # Cache miss: Compute and store the result
                result = func(*args, **kwargs)
                with self.cache as reference:
                    reference.set(key, result)
                    print(f"Cache miss for {func.__name__}{args}. Result cached.")
                    # Show cache contents
                    print(f"key = {reference.get(key)}")
                
            return result

        # Expose cache management methods
        def clear_cache():
            """Clear the cache."""
            CacheIt.cache.clear()
            print("Cache cleared.")

        def get_cache():
            """Get the keys stored in the cache."""
            return list(CacheIt.cache.iterkeys())

        wrapper.clear_cache = clear_cache
        wrapper.get_cache = get_cache

        return wrapper


# Main function to test the decorator
if __name__ == '__main__':
    
    # Usage
    @CacheIt(max_duration=60)
    def compute_square(x):
        """Compute the square of a number."""
        return x * x

    # Test the decorator
    print(f"compute_square(2) = {compute_square(2)} - Cache miss")  # Cache miss
    print('---')
    print(f"compute_square(2) = {compute_square(2)} - Cache hit")  # Cache hit
    print('---')
    print(f"compute_square(3) = {compute_square(3)} - Cache miss")  # Cache miss
    print('---')
    print(f"compute_square(2) = {compute_square(2)} - Cache hit")  # Cache hit
    print('---')
    # Check and clear the cache
    print(f"Cache before clearing: {compute_square.get_cache()}")
    compute_square.clear_cache()
    print(f"Cache after clearing: {compute_square.get_cache()}")
