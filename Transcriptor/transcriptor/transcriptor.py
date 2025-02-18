#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import whisper
import torch
import subprocess
import logging
import gc
import warnings
from pynput.keyboard import Key, Listener
from pydub import AudioSegment
from tenacity import retry, stop_after_attempt
from .microphonerecorder import MicrophoneRecorder

class Transcriptor:
    """
    A class to handle transcription of audio files using Whisper.
    """

    # Model sizes for Whisper
    # - "tiny" (~0.5GB RAM) - Fastest option
    # - "base" (~1GB RAM) - Good balance
    # - "small" (~2GB RAM) - Best balance
    # - "medium" (~5GB RAM) - Better accuracy
    # - "large" (~10GB RAM) - Best accuracy
    MODEL_SIZES = ["tiny", "base", "small", "medium", "large"]

    # Use Metal Performance Shaders (MPS) for memory efficiency
    USE_TORCH_MPS = False
    
    def __init__(self, model_size: str = "medium", language: str = "fr") -> None:
        """
        Initialize the transcriptor.
        ---
        Parameters:
        - model_size (str): Whisper model size ("tiny", "base", "small", "medium", "large")
        - language (str): Language code for transcription
        """

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.language = language
        
        # Check model size
        if model_size not in self.MODEL_SIZES:
            raise ValueError(f"Invalid model size: {model_size} (choose from {self.MODEL_SIZES})")

        # Message to user
        self.logger.info(f"Loading Whisper model: {model_size}")
        print(f"Loading Whisper model: {model_size}")

        # Load the Whisper model
        try:
            # Apple Silicon optimizations
            if self.USE_TORCH_MPS and torch.backends.mps.is_available():
                device = "mps"
                # Message to user
                self.logger.info("Using Metal Performance Shaders (MPS) for memory efficiency")
                print("Using Metal Performance Shaders (MPS) for memory efficiency")
                # MPS-specific configuration for memory efficiency and numerical stability
                torch.mps.set_per_process_memory_fraction(1.0)
                torch._C._jit_set_texpr_fuser_enabled(False)
            else:
                # Use CPU if MPS is not available
                device = "cpu"
                # Message to user
                self.logger.info("Using CPU for inference")
                print("Using CPU for inference")
            
            # Ignore warnings for FP16 on CPU
            if device == "cpu":
                warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

            # Configure for MPS with memory efficiency
            self.model = whisper.load_model(
                model_size,
                device=device,
                in_memory=True,  # Better for Apple SSDs
            )
            
            # MPS-specific configuration
            if device == "mps":
                torch.mps.set_per_process_memory_fraction(0.5)  # Prevent memory overload
                torch.set_flush_denormal(True)  # Improve numerical stability
        except Exception as e:
            # Print error message
            self.logger.error(f"Failed to load Whisper model: {e}")
            print(f"Failed to load Whisper model: {e}")
            raise
        
        # Initialize the recorder with the speech detection callback
        self.recorder = MicrophoneRecorder(self.handle_speech_detected)
    
    def handle_speech_detected(self, audio_file: str) -> None:
        """
        Handle detected speech by transcribing and pasting.
        ---
        Parameters:
        - audio_file (str): Path to the audio file
        """
        try:
            # Transcribe and paste the audio file
            transcribed_text = self.transcribe(audio_file)
            # Paste to MacOS clipboard
            self.paste_to_macos(transcribed_text)
        except Exception as e:
            self.logger.error(f"Error handling speech: {e}")

    @retry(stop=stop_after_attempt(3))
    def transcribe(self, audio_file: str) -> str:
        """
        Transcribe the audio file and paste the result.
        ---
        Parameters:
        - audio_file (str): The path to the audio file.
        ---
        Returns:
        - str: The transcribed text
        """
        try:
            # Normalize audio to -20dBFS
            audio = AudioSegment.from_wav(audio_file)
            audio = audio.normalize(headroom=20)
            normalized_file = "normalized.wav"
            audio.export(normalized_file, format="wav")

            # Transcribe the audio file
            result = self.model.transcribe(
                audio_file,                         # Path to the audio file
                language=self.language,             # Language code
                temperature=0.2,                    # Less random variations
                beam_size=5,                        # Better for MPS parallelization
                fp16=False,                         # MPS currently works better with fp32
                patience=1.5,                       # Apple Silicon-specific optimization
                compression_ratio_threshold=2.5     # Filter low-quality segments
            )

            # Normalize the text
            transcribed_text = result["text"].strip()
            transcribed_text = " ".join(result["text"].strip().split())  # Remove extra spaces
            transcribed_text = transcribed_text.capitalize() + "."  # Basic punctuation

            # Message to user
            self.logger.info("Transcription completed")
            print(f"\nTranscribed text: {transcribed_text}")

            # Return the transcribed text
            return transcribed_text
        except Exception as e:
            self.logger.error(f"Error in transcription: {e}")
            raise
        finally:
            # Clean up memory
            gc.collect()
            # MPS-specific memory cleanup
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()

    @staticmethod
    def paste_to_macos(text: str) -> bool:
        """
        Use pbcopy to paste text on MacOS.
        ---
        Parameters:
        - text (str): The text to paste.
        ---
        Returns:
        - bool: True if successful.
        """
        # Check if the text is not empty
        if text:
            try:
                # Copy to clipboard
                process = subprocess.Popen('pbcopy', stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
                
                # Paste using AppleScript
                apple_script = '''
                tell application "System Events"
                    keystroke "v" using command down
                end tell
                '''
                subprocess.run(['osascript', '-e', apple_script], check=True)
                return True
            except Exception as e:
                logging.error(f"Error pasting: {e}")
                raise
        return False

    @staticmethod
    def on_press(key: Key) -> bool:
        """
        Listener callback for key press events.
        ---
        Parameters:
        - key (Key): The key that was pressed.
        ---
        Returns:
        - bool: False to stop the listener.
        """

        # Stop the listener if 'esc' is pressed
        return False if key == Key.esc else True

    def start(self) -> None:
        """
        Start the voice-activated transcription system.
        """
        try:
            # Start the recording thread in the background
            recording_thread = threading.Thread(target=self.recorder.start_recording, daemon=True)
            recording_thread.start()

            # Start the key listener    
            with Listener(on_press=self.on_press) as listener:
                listener.join()
            
            # Stop the recording
            self.recorder.stop_recording()
            recording_thread.join()
            
        except Exception as e:
            self.logger.error(f"Error in main: {e}")
            self.recorder.stop_recording()
            raise