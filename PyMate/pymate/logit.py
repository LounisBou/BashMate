#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import logging
import os
from typing import Optional

class LogIt:
    """
    A helper class to create and configure loggers.
    """

    def __init__(self, name: Optional[str] = None, level: Optional[int] = None, console: bool = True, file: bool = False):
        """
        Initialize the logger with the specified configuration.
        Args:
            name (str, optional): Name of the logger. Defaults to module name if not provided.
            level (int, optional): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            console (bool): If True, logs to the console.
            file (bool): If True, logs to a file named 'logit.log'.
        """
        
        # Check if LogIt directory exists
        self.name = name if name else __name__
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(level if level else logging.INFO)
        self.logger.propagate = False  # Avoid duplicate logs

        # Check if handlers are already added
        if not self.logger.hasHandlers():
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger.
        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger

# Main function to test the decorator
if __name__ == '__main__':
    
    # Usage
    logger = LogIt(name='MyLogger', level=logging.DEBUG, console=True, file=True).get_logger()
    
    # Test the logger
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")