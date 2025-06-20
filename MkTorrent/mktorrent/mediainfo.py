#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import json
from typing import Dict,  Set, Any

class MediaInfo:
    """
    Class to handle mediainfo analysis and data extraction from media files.
    """

    def __init__(self, file_path: str):
        """
        Initialize the MediaInfo object with a file path.
        
        :param file_path: str - Path to the media file to analyze
        """
        self.file_path = file_path
        self.info = self._run_mediainfo()
        self.metadata = self._extract_metadata()

    def _run_mediainfo(self) -> Dict[str, Any]:
        """
        Execute mediainfo on the file and return the parsed JSON output.
        
        :return: Dict[str, Any] - Parsed JSON data from mediainfo
        """
        try:
            result = subprocess.run(
                ['mediainfo', '--Output=JSON', self.file_path],
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running mediainfo: {e}")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error decoding JSON from mediainfo output")
            sys.exit(1)

    def _extract_metadata(self) -> Dict[str, Any]:
        """
        Extract relevant metadata from mediainfo results.
        
        :return: Dict[str, Any] - Dictionary containing extracted metadata
        """
        info: Dict[str, Any] = {}
        
        # Process only if media and track are in the info
        if 'media' in self.info and 'track' in self.info['media']:
            for track in self.info['media']['track']:
                if track['@type'] == 'General':
                    self._process_general_track(track, info)
                elif track['@type'] == 'Video':
                    self._process_video_track(track, info)
                elif track['@type'] == 'Audio':
                    self._process_audio_track(track, info)
                elif track['@type'] == 'Text':
                    self._process_text_track(track, info)
        
        # Process language tag
        self._process_language_tag(info)
        
        return info

    def _process_general_track(self, track: Dict[str, Any], info: Dict[str, Any]) -> None:
        """
        Process the General track from mediainfo.
        
        :param track: Dict[str, Any] - General track data
        :param info: Dict[str, Any] - Dictionary to update with extracted information
        """
        info['format'] = track.get('Format', 'Unknown')
        info['duration'] = track.get('Duration', 'Unknown')
        info['overall_bitrate'] = track.get('OverallBitRate', 'Unknown')
        info['movie_name'] = track.get('Movie_name', '')
        
        # Try to extract source from movie_name
        if 'movie_name' in track:
            sources = ['BluRay', 'HDTV', 'WEB-DL', 'WEBRip', 'DVDRip', 'BDRip', 'BRRip']
            for source in sources:
                if source.lower() in track['movie_name'].lower():
                    info['source'] = source
                    break
            else:
                info['source'] = 'Unknown'

    def _process_video_track(self, track: Dict[str, Any], info: Dict[str, Any]) -> None:
        """
        Process the Video track from mediainfo.
        
        :param track: Dict[str, Any] - Video track data
        :param info: Dict[str, Any] - Dictionary to update with extracted information
        """
        info['video_format'] = track.get('Format', 'Unknown')
        info['video_format_profile'] = track.get('Format_Profile', 'Unknown')
        
        # Detect HEVC/H.265 or AVC/H.264
        if 'Format' in track:
            if track['Format'] == 'HEVC':
                info['video_codec'] = 'HEVC (H.265)'
            elif track['Format'] == 'AVC':
                info['video_codec'] = 'AVC (H.264)'
            else:
                info['video_codec'] = track['Format']
                
        info['width'] = track.get('Width', 'Unknown')
        info['height'] = track.get('Height', 'Unknown')
        
        # Determine resolution
        if 'Width' in track and 'Height' in track:
            width = int(track['Width'])
            height = int(track['Height'])
            
            if height >= 2160:
                info['resolution'] = '4K'
            elif height >= 1080:
                info['resolution'] = '1080p'
            elif height >= 720:
                info['resolution'] = '720p'
            else:
                info['resolution'] = f"{height}p"
        
        info['frame_rate'] = track.get('FrameRate', 'Unknown')
        info['bit_depth'] = track.get('BitDepth', 'Unknown')

    def _process_audio_track(self, track: Dict[str, Any], info: Dict[str, Any]) -> None:
        """
        Process the Audio track from mediainfo.
        
        :param track: Dict[str, Any] - Audio track data
        :param info: Dict[str, Any] - Dictionary to update with extracted information
        """
        if 'audio_languages' not in info:
            info['audio_languages'] = []
            info['audio_codecs'] = []
        
        if 'Language' in track:
            info['audio_languages'].append(track['Language'])
        else:
            info['audio_languages'].append('Unknown')
        
        audio_codec = f"{track.get('Format', '')} {track.get('Channels', '').replace('channels', 'ch')}"
        info['audio_codecs'].append(audio_codec.strip())

    def _process_text_track(self, track: Dict[str, Any], info: Dict[str, Any]) -> None:
        """
        Process the Text track (subtitles) from mediainfo.
        
        :param track: Dict[str, Any] - Text track data
        :param info: Dict[str, Any] - Dictionary to update with extracted information
        """
        if 'subtitle_languages' not in info:
            info['subtitle_languages'] = []
            info['subtitle_formats'] = []
        
        if 'Language' in track:
            info['subtitle_languages'].append(track['Language'])
        else:
            info['subtitle_languages'].append('Unknown')
            
        info['subtitle_formats'].append(track.get('Format', 'Unknown'))

    def _process_language_tag(self, info: Dict[str, Any]) -> None:
        """
        Determine the language tag (MULTI, FRENCH, etc.) from audio languages.
        
        :param info: Dict[str, Any] - Dictionary to update with language tag
        """
        if 'audio_languages' in info:
            unique_languages: Set[str] = set(info['audio_languages'])
            if len(unique_languages) > 1:
                info['language_tag'] = 'MULTI'
            else:
                language_map = {
                    'French': 'FRENCH',
                    'English': 'ENGLISH',
                    'fr': 'FRENCH',
                    'en': 'ENGLISH',
                    'es': 'SPANISH',
                    'de': 'GERMAN',
                    'it': 'ITALIAN'
                }
                first_lang = list(unique_languages)[0]
                info['language_tag'] = language_map.get(first_lang, first_lang.upper())


if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print("Usage: mediainfo.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    media_info = MediaInfo(file_path)
    print(json.dumps(media_info.metadata, indent=4))
