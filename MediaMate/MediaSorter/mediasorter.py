#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os
import shutil
import sys
from typing import List

class MediaSorter:
    """
    A class to sort media files into movies and TV shows directories based on their filename and extension.
    The class can clean filenames, pack files into directories, and sort them accordingly.
    """

    # DEBUG
    DEBUG = True
    
    # Directories by file type
    SORTED_DIR = {
        "movie": "001-MOVIES",
        "tvshow": "002-TVSHOWS",
        "ebook": "003-EBOOKS",
        "audio": "004-AUDIO",
        "app": "005-APPS",
        "android": "006-ANDROID",
    }

    # Extensions by file type
    EXTENSIONS = {
        "media": [
            "avi", "mkv", "mp4", "mpg", "mpeg", "mov", "wmv", "flv", "webm", "m4v",
            "3gp", "3g2", "asf", "rm", "swf", "vob", "ts", "m2ts", "mts", "m2t",
            "m4p", "m4b", "m4r", "m4a", "f4v", "f4a", "f4b", "f4p", "f4r", "ogg",
            "ogv", "oga", "ogx", "ogm", "spx", "opus", "flac", "wav", "mp3", "wma",
            "aac", "ac3", "dts", "pcm", "mka", "mks", "weba", "ra", "rmvb"
        ],
        "archive": ["zip", "rar", "7z", "tar", "gz", "bz2", "xz"],
        "image": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
        "subtitle": ["srt", "sub", "sbv", "vtt"],
        "ebook": ["pdf", "epub", "mobi", "azw", "azw3", "djvu", "cbz", "cbr", "fb2", "lit"],
        "document": ["doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "txt"],
        "app": ["exe", "msi", "dmg", "pkg", "deb", "rpm", "sh", "bat", "cmd"],
        "android": ["apk"],
        "iso": ["iso", "img", "bin", "cue", "nrg", "mdf", "mds", "ccd", "cif", "c2d"]
    }

    # Characters to delete from filenames
    CHARS_TO_DELETE: List[str] = ["5.1", "4.0", ".", "-", "_", "[", "]", "{", "}", "~", "+", "(", ")", "!"]

    # Words to delete from filenames
    WORDS_TO_DELETE = [
        "1080", "1080i", "1080p", "10bit", "1920x1080", "2160p", "2vf", "480p", "720p", "7sins",
        "4k", "4klight", "6ch", "aac", "aaclc", "abcollection", "ac 3", "ac3", "acc", "acool",
        "amzn", "ark01", "av1", "avc", "bbc", "bbt", "bdrip", "benh4", "bit", "bluray", "bluray1080p",
        "brrip", "btt", "buret", "ccats", "ch", "chris44", "custom", "darkjuju", "dd", "ddp",
        "directors cut", "dl", "dolby vision", "dread team", "dts", "dvdrip", "dvd rip", "eac3", 
        "eaulive", "en", "eng", "extended", "extreme", "fasandraeberne", "final cut", "flaskepost",
        "fr", "fre", "french", "french(vff)", "frosties", "ftmvhd", "fw", "gbx", "ght", "ghz", 
        "gismo65", "gwen", "h264", "h265", "h4s5s", "hd", "hdl", "hdlight", "hdma", "hdr", "hdtv", 
        "he", "hevc", "hush", "integral", "integrale", "internal", "jiheff", "k7", "kaf", "kfl", 
        "kvinden", "lazarus", "lcds", "libertad", "luminus", "mhd", "mhdgz", "mkv", "mm91", "moe", 
        "mtl666", "multi", "multi3", "nf", "noex", "nobodyperfect", "non censurée", "notag", "nyu", 
        "owii", "p4t4t3", "pop", "pophd", "Portos", "portos", "qtz", "remastered", "romkent", "se7en", 
        "serqph", "shc23", "slayer", "slay3r", "srt", "stereo", "tf", "title1", "tonyk", "tr", 
        "truefrench", "trunkdu92", "tvwh0res", "unrated", "uptopol", "utt", "version", "vf", "vf2", 
        "vff", "vfi", "vfq", "vlis", "vmpp", "vo", "vof", "vost", "vostfr", "web", "web dl", "webdl", 
        "webrip", "x264", "x265", "xvid", "zeusfaber", "zone80", "zza"
    ]

    @staticmethod
    def get_file_extension(filename: str) -> str:
        """
        Gets the extension of a file based on its filename.

        :param filename: Name of the file.
        :return: The extension of the file.
        """
        return filename.split('.')[-1].lower()

    @staticmethod
    def is_media(filename: str) -> bool:
        """
        Checks if a file is a media file based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is a media file, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["media"]
    
    @staticmethod
    def is_movie(filename: str) -> bool:
        """
        Determines if a file is a movie if it is a media file and not a TV show.

        :param filename: Name of the file to check.
        :return: True if the file is identified as a movie, False otherwise.
        """
        
        filename_lower = filename.lower()
        if not MediaSorter.is_media(filename_lower):
            return False
        return not MediaSorter.is_tv_show(filename_lower)

    @staticmethod
    def is_tv_show(filename: str) -> bool:
        """
        Determines if a file is a TV show based on the filename pattern (SXXEXX).

        :param filename: Name of the file to check.
        :return: True if the file is identified as a TV show, False otherwise.
        """
        filename_lower = filename.lower()
        if not MediaSorter.is_media(filename_lower):
            return False
        return 's' in filename_lower and 'e' in filename_lower
    
    @staticmethod
    def is_ebook(filename: str) -> bool:
        """
        Determines if a file is an ebook based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is identified as an ebook, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["ebook"]

    
    @staticmethod
    def is_audio(filename: str) -> bool:
        """
        Determines if a file is an audio file based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is identified as an audio file, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["audio"]
    
    @staticmethod
    def is_app(filename: str) -> bool:
        """
        Determines if a file is an application based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is identified as an application, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["app"]
    
    @staticmethod
    def is_android(filename: str) -> bool:
        """
        Determines if a file is an Android application based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is identified as an Android application, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["android"]
    
    @staticmethod
    def is_archive(filename: str) -> bool:
        """
        Determines if a file is an archive based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is identified as an archive, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["archive"]
    
    @staticmethod
    def is_image(filename: str) -> bool:
        """
        Determines if a file is an image based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is identified as an image, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["image"]
    
    @staticmethod
    def is_subtitle(filename: str) -> bool:
        """
        Determines if a file is a subtitle based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is identified as a subtitle, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["subtitle"]
    
    @staticmethod
    def is_document(filename: str) -> bool:
        """
        Determines if a file is a document based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is identified as a document, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["document"]
    
    @staticmethod
    def is_iso(filename: str) -> bool:
        """
        Determines if a file is an ISO image based on its extension.

        :param filename: Name of the file to check.
        :return: True if the file is identified as an ISO image, False otherwise.
        """
        return MediaSorter.get_file_extension(filename) in MediaSorter.EXTENSIONS["iso"]
    
    @staticmethod
    def is_sorted_dir(dirpath: str) -> bool:
        """
        Determines if a directory is a sorted directory.

        :param dirpath: The path of the directory to check.
        :return: True if the directory is a sorted directory, False otherwise.
        """
        return os.path.basename(dirpath) in MediaSorter.SORTED_DIR.values()

    @staticmethod
    def clean_filename_chars(filename: str) -> str:
        """
        Cleans unwanted characters from the filename.

        :param filename: The original filename.
        :return: The filename with unwanted characters removed.
        """
        for char in MediaSorter.CHARS_TO_DELETE:
            filename = filename.replace(char, ' ')
        return filename

    @staticmethod
    def clean_filename_words(filename: str) -> str:
        """
        Cleans unwanted words from the filename.

        :param filename: The original filename.
        :return: The filename with unwanted words removed.
        """
        for word in MediaSorter.WORDS_TO_DELETE:
            filename = filename.replace(f" {word} ", ' ')
        return filename.strip()

    @staticmethod
    def clean_filename(self, filename: str) -> str:
        """
        Cleans both unwanted characters and words from the filename.

        :param filename: The original filename.
        :return: The cleaned filename.
        """
        base, ext = os.path.splitext(filename)
        base = base.lower()
        base = MediaSorter.clean_filename_chars(base)
        base = MediaSorter.clean_filename_words(base)
        return base + ext
    
    @staticmethod
    def get_cleaned_filename(filepath: str) -> str:
        """
        Gets the cleaned filename of a file.

        :param filepath: The full path of the file.
        :return: The cleaned filename.
        """
        return MediaSorter.clean_filename(os.path.basename(filepath))
    
    @staticmethod
    def get_cleaned_basename(filepath: str) -> str:
        """
        Gets the cleaned basename of a file.

        :param filepath: The full path of the file.
        :return: The cleaned basename.
        """
        cleaned_name = MediaSorter.get_cleaned_filename(filepath)
        base, _ = os.path.splitext(cleaned_name)
        return base        

    @staticmethod
    def pack(filepath: str) -> None:
        """
        Packs a media file into a directory named after the cleaned basename.

        :param filepath: The full path of the file to pack.
        :return: None
        """
        if os.path.isfile(filepath):
            cleaned_name = MediaSorter.clean_filename(os.path.basename(filepath))
            dir_name = cleaned_name.rsplit('.', 1)[0]
            target_dir = os.path.join(os.path.dirname(filepath), dir_name)
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(target_dir, os.path.basename(filepath)))

    @staticmethod
    def unpack(dirpath: str) -> None:
        """
        Unpacks all files from a directory into the parent directory.

        :param dirpath: The path of the directory to unpack.
        :return: None
        """
        if os.path.isdir(dirpath):
            for filename in os.listdir(dirpath):
                file_path = os.path.join(dirpath, filename)
                if os.path.isfile(file_path):
                    shutil.move(file_path, MediaSorter.TOSORT_PATH)
            os.rmdir(dirpath)

    @staticmethod
    def sort(dirpath: str) -> None:
        """
        Sorts directories into either the corresponding file type directory.

        :param dirpath: The path of the directory to sort.
        :return: None
        """
        target_dir = os.path.join(MediaSorter.TOSORT_PATH, MediaSorter.TOSORT_TVSHOWS if MediaSorter.is_tv_show(dirpath) else MediaSorter.TOSORT_MOVIES)
        os.makedirs(target_dir, exist_ok=True)
        shutil.move(dirpath, target_dir)

    @staticmethod
    def process(dirpath: str) -> None:
        """
        Processes all directories and files in the 'ToSort' directory. Unpacks, packs, and sorts media files.

        :param dirpath: The path of the directory to process.
        :return: None
        """
        for element in os.listdir(dirpath):
            # Check if element is a directory
            element_path = os.path.join(dirpath, element)
            if os.path.isdir(element_path):
                # Do not process the sorted directories
                if MediaSorter.is_sorted_dir(element_path):
                    continue
                # Process the directory
                MediaSorter.unpack(element_path)
                MediaSorter.pack(element_path)
                MediaSorter.sort(element_path)

### Main program ###
if __name__ == "__main__":
    # Check first command-line argument to see if it is a directory
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        MediaSorter().process(sys.argv[1])
    else:
        print("Please provide a valid directory path as an argument.")
        sys.exit(1)