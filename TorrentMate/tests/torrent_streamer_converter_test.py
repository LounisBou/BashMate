#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from torrentmate import TorrentStreamerConverter
import pytest

def test_torrent_streamer_converter():

    # Define the source torrent file
    source = 'big-buck-bunny.torrent'
    # Define the output directory
    output_directory = 'output'
    # Define the maximum number of simultaneous conversions
    max_simultaneous_conversions = 1
    # Define the pause threshold
    pause_threshold = 0.1
    # Define the FFmpeg parameters
    ffmpeg_params = '-c:v libx264 -crf 23 -c:a aac -strict -2'

    # Instantiate the TorrentStreamerConverter with the parsed arguments
    streamer_converter = TorrentStreamerConverter(
        source=source,
        output_directory=output_directory,
        max_simultaneous_conversions=max_simultaneous_conversions,
        pause_threshold=pause_threshold,
        ffmpeg_params=ffmpeg_params if ffmpeg_params else None
    )

    # Start the conversion process
    streamer_converter.start()

    # Test if converted file is created
    #assert 
    