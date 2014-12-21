#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

from setuptools import find_packages, setup


with open(os.path.join("google_speech", "__init__.py"), "rt") as f:
  version = re.search("__version__ = \"([^\"]+)\"", f.read()).group(1)

with open("requirements.txt", "rt") as f:
  requirements = f.read().splitlines()

try:
  import pypandoc
  readme = pypandoc.convert("README.md", "rst")
except ImportError:
  with open("README.md", "rt") as f:
    readme = f.read()

setup(name="google_speech",
      version=version,
      author="desbma",
      packages=find_packages(),
      entry_points={"console_scripts": ["google_speech = google_speech:cl_main"]},
      test_suite="tests",
      install_requires=requirements,
      description="Read text using Google voice",
      long_description=readme,
      url="https://github.com/desbma/GoogleSpeech",
      download_url="https://github.com/desbma/GoogleSpeech/archive/%s.tar.gz" % (version),
      keywords=["speech", "audio", "synthesis", "voice", "google"],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Environment :: Console",
                   "Intended Audience :: Developers",
                   "Intended Audience :: End Users/Desktop",
                   "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3 :: Only",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
                   "Topic :: Multimedia :: Sound/Audio :: Speech",
                   "Topic :: Utilities"])
