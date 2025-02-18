#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import whisper
import subprocess
from pynput.keyboard import Key, Listener
import logging
from .microphonerecorder import MicrophoneRecorder

class Transcriptor:
    """
    A class to handle transcription of audio files using Whisper.
    """
    
    def __init__(self, model_size: str = "base", language: str = "fr") -> None:
        """
        Initialize the transcriptor.
        
        Parameters:
        - model_size (str): Whisper model size ("tiny", "base", "small", "medium", "large")
        - language (str): Language code for transcription
        """
        self.logger = logging.getLogger(__name__)
        self.language = language
        
        # Load the Whisper model
        try:
            self.logger.info(f"Loading Whisper model: {model_size}")
            self.model = whisper.load_model(model_size)
        except Exception as e:
            self.logger.error(f"Failed to load Whisper model: {e}")
            raise
        
        # Initialize the recorder with the speech detection callback
        self.recorder = MicrophoneRecorder(self.handle_speech_detected)
    
    def handle_speech_detected(self, audio_file: str) -> None:
        """
        Handle detected speech by transcribing and pasting.
        
        Parameters:
        - audio_file (str): Path to the audio file
        """
        try:
            self.transcribe_and_paste(audio_file)
        except Exception as e:
            self.logger.error(f"Error handling speech: {e}")

    def transcribe_and_paste(self, audio_file: str) -> None:
        """
        Transcribe the audio file and paste the result.
        
        Parameters:
        - audio_file (str): The path to the audio file.
        """
        try:
            result = self.model.transcribe(audio_file, language=self.language)
            transcribed_text = result["text"].strip()
            self.logger.info("Transcription completed")
            print(f"\nTranscribed text: {transcribed_text}")
            
            self.paste_to_macos(transcribed_text)
        except Exception as e:
            self.logger.error(f"Error in transcription: {e}")
            raise

    @staticmethod
    def paste_to_macos(text: str) -> None:
        """
        Use pbcopy to paste text on MacOS.
        
        Parameters:
        - text (str): The text to paste.
        """
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
        except Exception as e:
            logging.error(f"Error pasting: {e}")
            raise

    @staticmethod
    def on_press(key: Key) -> bool:
        """
        Listener callback for key press events.
        
        Parameters:
        - key (Key): The key that was pressed.
        
        Returns:
        - bool: False to stop the listener.
        """
        return False if key == Key.esc else True

    def start(self) -> None:
        """Start the voice-activated transcription system."""
        try:
            recording_thread = threading.Thread(target=self.recorder.start_recording)
            recording_thread.start()
            
            with Listener(on_press=self.on_press) as listener:
                listener.join()
            
            self.recorder.stop_recording()
            recording_thread.join()
            
        except Exception as e:
            self.logger.error(f"Error in main: {e}")
            self.recorder.stop_recording()
            raise