#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="mktorrent",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    
    # Metadata
    author="MkTorrent Creator",
    author_email="your.email@example.com",
    description="A tool to create torrent files, NFO files, and BBCode descriptions for media content",
    long_description=open("README.md").read() if hasattr(__file__, "__file__") else "",
    long_description_content_type="text/markdown",
    keywords="torrent, nfo, bbcode, media, mediainfo",
    url="https://github.com/lounisbou/mktorrent",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia",
        "Topic :: Utilities",
    ],
    
    # Entry points
    entry_points={
        "console_scripts": [
            "mktorrent-creator=mktorrent.mktorrent:main",
        ],
    },

    
    # Python requirements
    python_requires=">=3.6",
)