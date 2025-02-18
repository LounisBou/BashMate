#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import wave
import pyaudio
import threading
from datetime import datetime
import whisper
import threading
import subprocess
from pynput.keyboard import Key, Listener
from .voicedetector import VoiceDetector

class Transcriptor:
    
    """
    A class to record audio and transcribe the audio files using the Whisper model.
    """

    # Path to the audio file directory
    AUDIO_DIR = "__audio__"
    # Size of each audio chunk
    CHUNK = 1024
    # Audio format
    FORMAT = pyaudio.paInt16
    # Number of audio channels
    CHANNELS = 1
    # Audio sample rate
    RATE = 44100
    # Silence limit in seconds
    SILENCE_LIMIT = 2
    # Previous audio limit in seconds
    PREV_AUDIO = 0.5

    def __init__(self) -> None:
        """
        Initialize the microphone recorder and transcriptor.
        """
        self.recording = False
        self.frames = []
        self.vad = VoiceDetector()
        self.silence_frames = 0
        self.prev_audio = []
        self.stop_flag = threading.Event()

        # Load the Whisper model
        self.model = whisper.load_model("base")

    def start_recording(self) -> None:
        """
        Start recording audio from the microphone.
        """
        self.recording = True
        self.frames = []
        self.silence_frames = 0
        self.prev_audio = []
        self.p = pyaudio.PyAudio()
        
        # Find the correct input device
        device_index = None
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                device_index = i
                break
        
        # Check if a device was found
        if device_index is None:
            raise Exception("No input device found!")
        
        # Open the audio stream
        self.stream = self.p.open(format=self.FORMAT,
                                channels=self.CHANNELS,
                                rate=self.RATE,
                                input=True,
                                input_device_index=device_index,
                                frames_per_buffer=self.CHUNK)
        
        # Message to user
        print("Listening for speech... (Press 'esc' to stop)")
        
        # Start the recording loop
        num_prev_chunks = int(self.PREV_AUDIO * self.RATE / self.CHUNK)
        while not self.stop_flag.is_set():
            try:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                is_speech = self.vad.is_speech(data)
                
                if not is_speech:
                    self.silence_frames += 1
                    if not self.frames:
                        self.prev_audio.append(data)
                        if len(self.prev_audio) > num_prev_chunks:
                            self.prev_audio.pop(0)
                else:
                    if not self.frames:
                        print("Speech detected! Recording...")
                        self.frames.extend(self.prev_audio)
                    self.silence_frames = 0
                    
                if self.frames or is_speech:
                    self.frames.append(data)
                
                if self.silence_frames > int(self.SILENCE_LIMIT * self.RATE / self.CHUNK) and self.frames:
                    print("Silence detected, processing speech...")
                    self.process_recording()
                    self.frames = []
                    self.silence_frames = 0
                    print("\nListening for speech... (Press 'esc' to stop)")
                    
            except Exception as e:
                print(f"Error in recording loop: {e}")
                break
    
    def process_recording(self) -> None:
        """
        Process the recorded audio and transcribe it.
        """

        # Check if there are frames
        if not self.frames:
            return
        
        # Save the audio to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = f"audio_{timestamp}.wav"
        self.save_audio(audio_file)

        # Transcribe the audio
        print("Transcribing...")
        self.transcribe_and_paste(audio_file)
        
        # Remove the audio file
        try:
            os.remove(audio_file)
        except Exception as e:
            print(f"Error removing audio file: {e}")

    def transcribe_and_paste(self, audio_file: str) -> None:
        """
        Transcribe the audio file and paste the result.
        -----
        Parameters:
        - audio_file (str): The path to the audio file.
        """
        try:
            result = self.model.transcribe(audio_file, language='fr')
            transcribed_text = result["text"].strip()
            print(f"\nTranscribed text: {transcribed_text}")
            
            # Use MacOS native clipboard and paste
            self.paste_to_macos(transcribed_text)
        except Exception as e:
            print(f"Error in transcription: {e}")
            
            
    def stop_recording(self) -> None:
        """
        Stop the recording.
        """

        # Set the stop flag
        self.stop_flag.set()
        self.recording = False
        if hasattr(self, 'stream'):
            try:
                self.stream.stop_stream()
                self.stream.close()
                self.p.terminate()
            except Exception as e:
                print(f"Error stopping recording: {e}")
        
    def save_audio(self, filename: str) -> None:
        """
        Save the recorded audio to a WAV file.
        ---
        Parameters:
        - filename (str): The filename to save the audio.
        """

        # Check if there are frames
        if self.frames:
            try:
                wf = wave.open(filename, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(self.frames))
                wf.close()
            except Exception as e:
                print(f"Error saving audio: {e}")
    
    @staticmethod
    def paste_to_macos(text: str) -> None:
        """
        Use pbcopy to paste text on MacOS
        -----
        Parameters:
        - text (str): The text to paste.
        """
        try:
            process = subprocess.Popen('pbcopy', stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            
            # Execute osascript to paste
            apple_script = '''
            tell application "System Events"
                keystroke "v" using command down
            end tell
            '''
            subprocess.run(['osascript', '-e', apple_script])
        except Exception as e:
            print(f"Error pasting: {e}")

    @staticmethod
    def on_press(key: Key) -> bool:
        """
        Listener callback for key press events.
        -----
        Parameters:
        - key (Key): The key that was pressed.
        -----
        Returns:
        - bool: False to stop the listener.
        """
        if key == Key.esc:
            return False

    def main(self) -> None:

        """ 
        Start the voice-activated recording system.
        """
        
        # Start the recording thread
        recording_thread = threading.Thread(target=self.start_recording)
        recording_thread.start()
        
        # Start the keyboard listener
        with Listener(on_press=self.on_press) as listener:
            listener.join()
        
        # Stop the recording threadd'abord nous débâtir ! que nous débâires de 4 immensely
        self.stop_recording()
        # Wait for the thread to finish
        recording_thread.join()