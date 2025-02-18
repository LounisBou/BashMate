#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import wave
import pyaudio
import threading
from datetime import datetime
from .voicedetector import VoiceDetector
import logging
from typing import Callable

class MicrophoneRecorder:
    """
    A class to handle microphone recording with voice activity detection.
    """
    
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
    
    def __init__(self, on_speech_detected: Callable[[str], None]) -> None:
        """
        Initialize the microphone recorder.
        
        Parameters:
        - on_speech_detected: Callback function to handle processed audio files
        """
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self.recording = False
        self.frames = []
        self.vad = VoiceDetector()
        self.silence_frames = 0
        self.prev_audio = []
        self.stop_flag = threading.Event()
        self.on_speech_detected = on_speech_detected
        
    def _get_input_device(self) -> int:
        """
        Find the appropriate input device.
        
        Returns:
        - int: Device index
        """
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                self.logger.info(f"Using input device: {device_info['name']}")
                return i
        raise Exception("No input device found!")

    def start_recording(self) -> None:
        """
        Start recording audio from the microphone.
        """
        self.recording = True
        self.frames = []
        self.silence_frames = 0
        self.prev_audio = []
        self.p = pyaudio.PyAudio()
        
        try:
            # Find the correct input device
            device_index = self._get_input_device()
            
            # Open the audio stream
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.CHUNK
            )
            
            self.logger.info("Started recording")
            print("Listening for speech... (Press 'esc' to stop)")
            
            self._record_loop()
            
        except Exception as e:
            self.logger.error(f"Error in recording: {e}")
            self.stop_recording()
            raise

    def _record_loop(self) -> None:
        """
        Main recording loop with voice activity detection.
        """
        num_prev_chunks = int(self.PREV_AUDIO * self.RATE / self.CHUNK)
        
        while not self.stop_flag.is_set():
            try:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                is_speech = self.vad.is_speech(data)
                
                if not is_speech:
                    self._handle_silence(data, num_prev_chunks)
                else:
                    self._handle_speech(data)
                    
            except Exception as e:
                self.logger.error(f"Error in recording loop: {e}")
                break

    def _handle_silence(self, data: bytes, num_prev_chunks: int) -> None:
        """Handle silent audio chunks."""
        self.silence_frames += 1
        if not self.frames:
            self.prev_audio.append(data)
            if len(self.prev_audio) > num_prev_chunks:
                self.prev_audio.pop(0)
        
        if self.silence_frames > int(self.SILENCE_LIMIT * self.RATE / self.CHUNK) and self.frames:
            self.logger.info("Silence detected, processing speech...")
            self._process_recording()
            self.frames = []
            self.silence_frames = 0
            print("\nListening for speech... (Press 'esc' to stop)")

    def _handle_speech(self, data: bytes) -> None:
        """Handle speech audio chunks."""
        if not self.frames:
            self.logger.info("Speech detected")
            print("Speech detected! Recording...")
            self.frames.extend(self.prev_audio)
        self.silence_frames = 0
        self.frames.append(data)

    def _process_recording(self) -> None:
        """Process the recorded audio."""
        if not self.frames:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = f"audio_{timestamp}.wav"
        
        try:
            self.save_audio(audio_file)
            self.on_speech_detected(audio_file)
        except Exception as e:
            self.logger.error(f"Error processing recording: {e}")
        finally:
            if os.path.exists(audio_file):
                os.remove(audio_file)

    def save_audio(self, filename: str) -> None:
        """
        Save the recorded audio to a WAV file.
        
        Parameters:
        - filename (str): The filename to save the audio.
        """
        if not self.frames:
            return
            
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(self.frames))
            self.logger.info(f"Saved audio to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving audio: {e}")
            raise

    def stop_recording(self) -> None:
        """Stop the recording and clean up resources."""
        self.stop_flag.set()
        self.recording = False
        
        if hasattr(self, 'stream'):
            try:
                self.stream.stop_stream()
                self.stream.close()
                self.p.terminate()
                self.logger.info("Recording stopped")
            except Exception as e:
                self.logger.error(f"Error stopping recording: {e}")

