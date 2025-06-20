#!/usr/bin/env python 
# -*- coding: utf-8 -*-

class LazyIt:
    """
    Decorator to evaluate a function only when its result is accessed, useful for expensive computations.
    """
    def __init__(self, func):
        self.func = func
        self.result = None
        self.evaluated = False
        
    def __get__(self, instance, owner):
        """Handle method binding for instance methods."""
        return functools.partial(self.__call__, instance)

    def __call__(self, *args, **kwargs):
        if not self.evaluated:
            self.result = self.func(*args, **kwargs)
            self.evaluated = True
        return self.result

# Main function to test the decorator
if __name__ == "__main__":
    
    @LazyIt
    def compute():
        print("Computing...")
        return 42

    # Test
    result = compute()
    print(result)  # Computing...
    print(result)  # No computation