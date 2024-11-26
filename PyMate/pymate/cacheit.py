#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from diskcache import Cache
from typing import Any, Optional
from pymate.saveit import SaveIt

class CacheIt:
    """
    A caching decorator for persistent caching across an entire project.
    By default, it uses diskcache. Optionally, it can use SaveIt as the backend.
    """
    
    # Class-level cache for diskcache
    cache = Cache('__cacheit__')
    
    def __init__(
        self, 
        max_duration: int = 3600, 
        backend: str = 'diskcache', 
        redis_config : Optional[dict] = None, 
        sqlite_db_name: str = 'cacheit'
    ):
        """
        Initialize the cache parameters.
        Arguments:
            max_duration (int): Cache duration in seconds.
            backend (str): 'redis', 'sqlite', or 'diskcache'.
            redis_config (dict): Redis connection details.
            sqlite_db_name (str): SQLite database name.
        """
        self.max_duration = max_duration
        self.saveit = None
        self.backend = backend.lower() if backend else None
        if self.backend not in ['redis', 'sqlite', 'diskcache']:
            raise ValueError("Backend must be either 'redis', 'sqlite', or 'diskcache'.")
        
        # Initialize SaveIt instance if backend is specified
        if self.backend in ['redis', 'sqlite']:
            self.saveit = SaveIt(backend=self.backend, redis_config=redis_config, sqlite_db_name=sqlite_db_name)
    
    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a unique cache key
            key = (func.__name__, args, frozenset(kwargs.items()))
            key_str = repr(key)  # Convert key to string for storage

            if self.saveit:
                # Use SaveIt as the backend
                if self.saveit.exists(key_str):
                    print(f"Cache hit for {func.__name__}{args}")
                    result = self.saveit.get(key_str)
                else:
                    result = func(*args, **kwargs)
                    self.saveit.set(key_str, result, expiry_seconds=self.max_duration)
                    print(f"Cache miss for {func.__name__}{args}. Result cached.")
            else:
                # Use diskcache as the backend
                if key in CacheIt.cache:
                    print(f"Cache hit for {func.__name__}{args}")
                    result = CacheIt.cache[key]
                else:
                    result = func(*args, **kwargs)
                    with CacheIt.cache as reference:
                        reference.set(key, result, expire=self.max_duration)
                        print(f"Cache miss for {func.__name__}{args}. Result cached.")
                # Note: No need to show cache contents here
                
            return result

        # Expose cache management methods
        def clear_cache():
            """Clear the cache."""
            if self.saveit:
                self.saveit.flush_all()
            else:
                CacheIt.cache.clear()
            print("Cache cleared.")

        def get_cache():
            """Get the keys stored in the cache."""
            if self.saveit:
                return self.saveit.get_all_keys()
            else:
                return list(CacheIt.cache.iterkeys())

        wrapper.clear_cache = clear_cache
        wrapper.get_cache = get_cache

        return wrapper


# Main function to test the decorator
if __name__ == '__main__':
    
    # DISKCACHE EXAMPLE
    print(f"\n{'='*10} DISKCACHE EXAMPLE {'='*10}")
    
    # Usage with diskcache backend
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
    
    
    # REDIS EXAMPLE
    print(f"\n{'='*10} REDIS EXAMPLE {'='*10}")
    
    # Usage with Redis backend
    @CacheIt(max_duration=60, backend='redis', redis_config={'host': 'localhost', 'port': 6379, 'db': 0})
    def compute_cube(x):
        """Compute the cube of a number."""
        return x ** 3

    # Test the decorator
    print(f"compute_cube(2) = {compute_cube(2)}")  # Cache miss
    print('---')
    print(f"compute_cube(2) = {compute_cube(2)}")  # Cache hit
    print('---')
    # Check and clear the cache
    print(f"Cache before clearing: {compute_cube.get_cache()}")
    compute_cube.clear_cache()
    print(f"Cache after clearing: {compute_cube.get_cache()}")
    
    # SQLITE EXAMPLE
    print(f"\n{'='*10} SQLITE EXAMPLE {'='*10}")
    
    # Usage with SQLite backend
    @CacheIt(max_duration=60, backend='sqlite')
    def compute_power(x, y):
        """Compute x raised to the power y."""
        return x ** y

    # Test the decorator
    print(f"compute_power(2, 3) = {compute_power(2, 3)}")  # Cache miss
    print('---')
    print(f"compute_power(2, 3) = {compute_power(2, 3)}")  # Cache hit
    print('---')
    # Check and clear the cache
    print(f"Cache before clearing: {compute_power.get_cache()}")
    compute_power.clear_cache()
    print(f"Cache after clearing: {compute_power.get_cache()}")
