#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from transcriptor import Transcriptor

if __name__ == "__main__":

    """
    Main function to start the voice-activated recording system
    """
    
    try:
        # Message to user
        print("Starting voice-activated recording system...")
        print("The system will automatically detect when you start and stop speaking.")
        print("Press 'esc' at any time to exit.")

        # Initialize the transcriptor
        transcriptor = Transcriptor()

        # Run the main function
        transcriptor.start()

    except KeyboardInterrupt:
        print("\nProgram terminated by user")