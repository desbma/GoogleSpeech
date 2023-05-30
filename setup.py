#!/usr/bin/env python3

""" Package setup. """

import os
import re
import sys

from setuptools import find_packages, setup

if sys.hexversion < 0x3070000:
    print("Python version %s is unsupported, >= 3.7.0 is needed" % (".".join(map(str, sys.version_info[:3]))))
    exit(1)

with open(os.path.join("google_speech", "__init__.py"), "rt") as f:
    match = re.search('__version__ = "([^"]+)"', f.read())
    assert match is not None
    version = match.group(1)

with open("requirements.txt", "rt") as f:
    requirements = f.read().splitlines()

with open("README.md", "rt") as f:
    readme = f.read()

setup(
    name="google_speech",
    version=version,
    author="desbma",
    packages=find_packages(exclude=("tests",)),
    entry_points={"console_scripts": ["google_speech = google_speech:cl_main"]},
    test_suite="tests",
    install_requires=requirements,
    description="Read text using Google Translate TTS API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/desbma/GoogleSpeech",
    download_url="https://github.com/desbma/GoogleSpeech/archive/%s.tar.gz" % (version),
    keywords=["speech", "audio", "synthesis", "voice", "google", "tts"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Utilities",
    ],
)
