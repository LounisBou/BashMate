#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from enum import Enum

class Colors(Enum):
    
    GREY = 'grey'
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'
    MAGENTA = 'magenta'
    CYAN = 'cyan'
    WHITE = 'white'
    
    
# Main function to test the enum
if __name__ == '__main__':
    
    print(f"Colors.RED: {Colors.RED}")
    print(f"Colors.RED.value: {Colors.RED.value}")
    print(f"Colors.RED.name: {Colors.RED.name}")
    print(f"Colors.RED == Colors.RED: {Colors.RED == Colors.RED}")
    print(f"Colors.RED == Colors.GREEN: {Colors.RED == Colors.GREEN}")
    print(f"Colors.RED == 'red': {Colors.RED == 'red'}")
    print(f"Colors.RED == 'Colors.RED': {Colors.RED == 'Colors.RED'}")