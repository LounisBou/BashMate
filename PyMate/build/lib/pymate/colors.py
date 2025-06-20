#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from enum import Enum

class Colors(Enum):
    
    """ Colors """
    GREY = 'grey'
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'
    MAGENTA = 'magenta'
    CYAN = 'cyan'
    WHITE = 'white'
    
    """ Light Colors """
    LIGHT_GREY = 'light_grey'
    LIGHT_RED = 'light_red'
    LIGHT_GREEN = 'light_green'
    LIGHT_YELLOW = 'light_yellow'
    LIGHT_BLUE = 'light_blue'
    LIGHT_MAGENTA = 'light_magenta'
    LIGHT_CYAN = 'light_cyan'
    
    """ Dark Colors """
    DARK_GREY = 'dark_grey'
    
    """ Highlights """
    ON_BLACK = 'on_black'
    ON_RED = 'on_red'
    ON_GREEN = 'on_green'
    ON_YELLOW = 'on_yellow'
    ON_BLUE = 'on_blue'
    ON_MAGENTA = 'on_magenta'
    ON_CYAN = 'on_cyan'
    ON_WHITE = 'on_white'
    
    """ Light Highlights """
    ON_LIGHT_GREY = 'on_light_grey'
    ON_LIGHT_RED = 'on_light_red'
    ON_LIGHT_GREEN = 'on_light_green'
    ON_LIGHT_YELLOW = 'on_light_yellow'
    ON_LIGHT_BLUE = 'on_light_blue'
    ON_LIGHT_MAGENTA = 'on_light_magenta'
    ON_LIGHT_CYAN = 'on_light_cyan'
    
    """ Dark Highlights """
    ON_DARK_GREY = 'on_dark_grey'
    
    """ Attributes """
    BOLD = 'bold'
    DARK = 'dark'
    UNDERLINE = 'underline'
    BLINK = 'blink'
    REVERSE = 'reverse'
    CONCEALED = 'concealed'
    STRIKE = 'strike'
    
    """ Reset """
    RESET = 'reset'
    
    """ Default """
    DEFAULT = 'default'
    
    
# Main function to test the enum
if __name__ == '__main__':
    
    print(f"Colors.RED: {Colors.RED}")
    print(f"Colors.RED.value: {Colors.RED.value}")
    print(f"Colors.RED.name: {Colors.RED.name}")
    print(f"Colors.RED == Colors.RED: {Colors.RED == Colors.RED}")
    print(f"Colors.RED == Colors.GREEN: {Colors.RED == Colors.GREEN}")
    print(f"Colors.RED == 'red': {Colors.RED == 'red'}")
    print(f"Colors.RED == 'Colors.RED': {Colors.RED == 'Colors.RED'}")