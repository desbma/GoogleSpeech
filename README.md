Google Speech
=============

[![Latest Version](https://img.shields.io/pypi/v/google_speech.svg?style=flat)](https://pypi.python.org/pypi/google_speech/)
[![Tests Status](https://img.shields.io/travis/desbma/GoogleSpeech/master.svg?label=tests&style=flat)](https://travis-ci.org/desbma/GoogleSpeech)
[![Coverage](https://img.shields.io/coveralls/desbma/GoogleSpeech/master.svg?style=flat)](https://coveralls.io/github/desbma/GoogleSpeech?branch=master)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/google_speech.svg?style=flat)](https://pypi.python.org/pypi/google_speech/)
[![License](https://img.shields.io/github/license/desbma/GoogleSpeech.svg?style=flat)](https://pypi.python.org/pypi/google_speech/)

Google Speech is a simple multiplatform command line tool to read text using Google Translate TTS (Text To Speech) API.


## Features

* Support 64 different languages
* Can read text without length limit
* Can read text from standard input
* Automatically pre download the next sentences while playing the current one to avoid long pauses between sentences
* Automatically store downloaded data in a local cache
* Can apply any [SoX effect](http://sox.sourceforge.net/sox.html#EFFECTS) to the audio while playing it


## Installation

Google Speech requires [Python](https://www.python.org/downloads/) >= 3.3.

### From PyPI (with PIP)

1. If you don't already have it, [install pip](http://www.pip-installer.org/en/latest/installing.html) for Python 3 (not needed if you are using Python >= 3.4)
2. Install Google Speech: `pip3 install google_speech`
3. Install [SoX](http://sox.sourceforge.net/), with MP3 support.
On Ubuntu and other Debian derivatives: `sudo apt-get install sox libsox-fmt-mp3`.
Windows users can [download binaries on the SoX website](http://sourceforge.net/projects/sox/files/sox/), once installed you also need to copy [libmad DLL](http://ossbuild.googlecode.com/svn/trunk/Shared/Build/Windows/Win32/bin/libmad-0.dll) in the directory where you have installed SoX, and to add this directory to your PATH environment variable.

### From source

1. If you don't already have it, [install setuptools](https://pypi.python.org/pypi/setuptools#installation-instructions) for Python 3
2. Clone this repository: `git clone https://github.com/desbma/GoogleSpeech`
3. Install Google Speech: `python3 setup.py install`
4. Install [SoX](http://sox.sourceforge.net/), with MP3 support.
On Ubuntu and other Debian derivatives: `sudo apt-get install sox libsox-fmt-mp3`.
Windows users can [download binaries on the SoX website](http://sourceforge.net/projects/sox/files/sox/), once installed you also need to copy [libmad DLL](http://ossbuild.googlecode.com/svn/trunk/Shared/Build/Windows/Win32/bin/libmad-0.dll) in the directory where you have installed SoX, and to add this directory to your PATH environment variable.


## Command line usage

Run `google_speech -h` to get full command line reference.

### Examples

* Plane stall alarm:

    `google_speech -l en stall -e delay 0.5 overdrive 20 repeat 5 speed 0.9 gain -5`

* Female robot voice (idea from [here](http://ubuntuforums.org/showthread.php?t=1813001&p=11090789#post11090789)):

    `google_speech -l en "Hello, I am a stupid robot voice" -e speed 0.9 overdrive 10 echo 0.8 0.7 6 0.7 echo 0.8 0.7 10 0.7 echo 0.8 0.7 12 0.7 echo 0.8 0.88 12 0.7 echo 0.8 0.88 30 0.7 echo 0.6 0.6 60 0.7`

On Unix systems, with Bash and pipes, you can be creative:

* Bash greetings:

    `google_speech -l en "Hello $USER, it is $(date)"`

* Countdown:

    `for i in {10..0}; do ( google_speech $i & ); sleep 1s; done`

* Read a Chuck Norris joke:

    `curl -s http://api.icndb.com/jokes/random/ | python3 -c 'import html.parser, json, sys; print(html.parser.HTMLParser().unescape(json.load(sys.stdin)["value"]["joke"]))' | google_speech -`


## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0-standalone.html)
