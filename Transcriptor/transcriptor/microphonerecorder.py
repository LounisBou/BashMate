#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wave
import pyaudio
import threading
from datetime import datetime
import webrtcvad
import logging
from typing import Callable
import tempfile

class MicrophoneRecorder:
    """
    A class to handle microphone recording with voice activity detection.
    """
    
    # Size of each audio chunk - Modified to match WebRTC VAD requirements
    CHUNK = 480  # Keep at 480 for 30ms at 16kHz
    # Audio format
    FORMAT = pyaudio.paInt16
    # Number of audio channels
    CHANNELS = 1
    # Audio sample rate - Changed to match WebRTC VAD requirements
    RATE = 16000  # WebRTC VAD only supports 8000, 16000, or 32000 Hz
    # Silence limit in seconds
    SILENCE_LIMIT = 1.0
    # Previous audio limit in seconds
    PREV_AUDIO = 0.8
    # Frame duration in milliseconds
    FRAME_DURATION = 30
    # Aggressiveness level of the VAD (0-3)
    AGGRESSIVENESS = 1
    # Default threshold for voice detection
    DEFAULT_THRESHOLD = 1500
    
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
        
        # Initialize variables
        self.recording = False
        self.frames = []
        self.silence_frames = 0
        self.prev_audio = []
        self.on_speech_detected = on_speech_detected

        # Initialize the WebRTC VAD
        self.vad = webrtcvad.Vad(self.AGGRESSIVENESS)
        
        # Create a stop flag
        self.stop_flag = threading.Event()

        # Initialize threshold
        self.threshold = self.DEFAULT_THRESHOLD
        
    def _get_input_device(self) -> int:
        """
        Find the appropriate input device.
        ---
        Returns:
        - int: Device index
        """
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                self.logger.info(f"Using input device: {device_info['name']}")
                return i
        raise Exception("No input device found!")

    def _record_loop(self) -> None:
        """
        Main recording loop with voice activity detection.
        """
        num_speech_frames = 0
        speech_detected = False
        
        while not self.stop_flag.is_set():
            try:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                
                # Check if this frame contains speech
                try:
                    is_speech = self.vad.is_speech(data, self.RATE)
                except Exception as e:
                    self.logger.error(f"VAD error: {e}")
                    continue
                
                if is_speech:
                    num_speech_frames += 1
                    if num_speech_frames >= 3 and not speech_detected:  # Require 3 consecutive speech frames
                        speech_detected = True
                        self.logger.info("Speech detected")
                        print("Speech detected! Recording...")
                    
                    if speech_detected:
                        self.frames.append(data)
                else:
                    if speech_detected:
                        self.silence_frames += 1
                        self.frames.append(data)
                        
                        # Stop recording after silence threshold
                        if self.silence_frames > int(self.SILENCE_LIMIT * self.RATE / self.CHUNK):
                            if len(self.frames) > 0:
                                self.logger.info("Silence detected, processing speech...")
                                self._process_recording()
                            speech_detected = False
                            num_speech_frames = 0
                            self.silence_frames = 0
                            self.frames = []
                            print("\nListening for speech... (Press 'esc' to stop)")
                    else:
                        num_speech_frames = 0
                        
            except Exception as e:
                self.logger.error(f"Error in recording loop: {e}")
                break

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
            
            # Message to user
            self.logger.info("Started recording")
            print("Listening for speech... (Press 'esc' to stop)")
            
            # Start the recording loop
            self._record_loop()
            
        except Exception as e:
            self.logger.error(f"Error in recording: {e}")
            self.stop_recording()
            raise

    def _process_recording(self) -> None:
        """
        Process the recorded audio.
        This function is called when silence is detected after speech.
        """
        if not self.frames:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                self.save_audio(tmpfile.name)
                self.on_speech_detected(tmpfile.name)
        except Exception as e:
            self.logger.error(f"Error processing recording: {e}")

    def save_audio(self, filename: str) -> None:
        """
        Save the recorded audio to a WAV file.
        ---
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
        """
        Stop the recording and clean up resources.
        """
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