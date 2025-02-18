#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class VoiceDetector:

    """
    A simple voice detector that uses root mean square (RMS) energy to detect speech.
    """

    def __init__(self) -> None:
        """
        Initialize the voice detector.
        """

        # Threshold for speech detection in RMS energy 
        self.THRESHOLD = 1500
        
    def is_speech(self, data_chunk: bytes) -> bool:
        """
        Check if the data chunk contains speech.
        ---
        Parameters:
        - data_chunk: The audio data chunk.
        ---
        Returns:
        - bool: True if speech is detected.
        """

        # Convert the data chunk to numpy array
        try:
            audio_data = np.frombuffer(data_chunk, dtype=np.int16)
            rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))) + 1e-10)
            return rms > self.THRESHOLD
        except Exception as e:
            print(f"Error in is_speech: {e}")
            return False
