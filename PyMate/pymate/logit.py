#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import logging
import os
from typing import Optional
from termcolor import colored
from pymate.colors import Colors
from pymate.infos import Infos

class LogIt:
    """
    A helper class to create and configure loggers.
    """

    def __init__(
        self, 
        name: Optional[str] = None, 
        level: Optional[int] = None, 
        console: bool = True, 
        file: bool = False, 
        format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ):
        """
        Initialize the logger with the specified configuration.
        Args:
            name (str, optional): Name of the logger. Defaults to module name if not provided.
            level (int, optional): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            console (bool): If True, logs to the console.
            file (bool): If True, logs to a file named 'logit.log'.
            format (str): Format of the log message.
        """
        
        # Check if name is provided
        if name is None:
            # Get executed script name
            name = Infos.get_script_package_name()
        
        # Check if LogIt directory exists
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(level if level else logging.INFO)
        self.logger.propagate = False  # Avoid duplicate logs

        # Check if handlers are already added
        if not self.logger.hasHandlers():
            formatter = logging.Formatter(format)

            # Add console handler
            if console:
                self._add_console_handler(formatter)

            # Add file handler
            if file:
                self._add_file_handler(formatter)

    def _add_console_handler(self, formatter: logging.Formatter):
        """
        Add a console handler to the logger.
        Args:
            formatter (logging.Formatter): Formatter for the handler.
        """
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(self, formatter: logging.Formatter):
        """
        Add a file handler to the logger.
        Args:
            formatter (logging.Formatter): Formatter for the handler.
        """
        directory = '__logit__'
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            file_handler = logging.FileHandler(os.path.join(directory, 'logit.log'))
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"Failed to create file handler: {e}")

    def debug(self, message: str, color: Colors = Colors.CYAN, attributs=[]) -> None:
        """
        Log a debug message.
        Args:
            message (str): The message to log.
            color (Colors): The color of the message.
        """
        self.logger.debug(colored(message, color.value, attrs=attributs))
        
    def info(self, message: str, color: Colors = Colors.WHITE, attributs: list = []) -> None:
        """
        Log an info message.
        Args:
            message (str): The message to log.
            color (Colors): The color of the message.
        """
        self.logger.info(colored(message, color.value, attrs=attributs))
    
    def warning(self, message: str, color: Colors = Colors.YELLOW, attributs: list = []) -> None:
        """
        Log a warning message.
        Args:
            message (str): The message to log.
            color (Colors): The color of the message.
        """
        self.logger.warning(colored(message, color.value, attrs=attributs))
        
    def warn(self, message: str, color: Colors = Colors.YELLOW, attributs: list = []) -> None:
        """
        Alias for warning.
        Args:
            message (str): The message to log.
            color (Colors): The color of the message.
        """
        self.warning(message, color=color, attrs=attributs)
        
    def error(self, message: str, color: Colors = Colors.RED, attributs: list = []) -> None:
        """
        Log an error message.
        Args:
            message (str): The message to log.
            color (Colors): The color of the message.
        """
        self.logger.error(colored(message, color.value, attrs=attributs))
        
    def critical(self, message: str, color: Colors = Colors.MAGENTA, attributs: list = []) -> None:
        """
        Log a critical message.
        Args:
            message (str): The message to log.
            color (Colors): The color of the message.
        """
        self.logger.critical(colored(message, color.value, attrs=attributs))
        
    def exception(self, message: str, color: Colors = Colors.RED, attributs: list = []) -> None:
        """
        Log an exception message.
        Args:
            message (str): The message to log.
            color (Colors): The color of the message.
        """
        self.logger.exception(colored(message, color.value, attrs=attributs))
        
    def separator(self, size: int = 100, color: Colors = Colors.WHITE, attributs=['bold']) -> None:
        """
        Log a separator.
        Args:
            size (int): The size of the separator.
            color (Colors): The color of the separator.
            attributs (list): The attributes of the separator.
        """
        self.logger.info(colored('-' * size, color.value, attrs=attributs))
        
    def line_break(self, nb_breaks: int = 1) -> None:
        """
        Log a line break.
        Args:
            nb_breaks (int): Number of line
        """
        for _ in range(nb_breaks):
            self.logger.info('')
        

# Main function to test the decorator
if __name__ == '__main__':
    
    # Usage
    logger = LogIt(level=logging.DEBUG, console=True, file=True)
    
    # Test the logger
    logger.separator()
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    logger.exception("This is an exception message.")
    logger.separator(100)
    logger.line_break()
    logger.separator(50)
    logger.line_break(2)
    logger.separator(25)
    logger.line_break(3)
    logger.separator(10)