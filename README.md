Google Speech
=============

Google Speech is a simple multiplatform command line tool to read text using Google Translate voice.


## Features

* Can read text without length limit
* Can read text from standard input
* Automatically pre download the next sentences while playing the current one to avoid long pauses between sentences
* Automatically store downloaded data in a local cache
* Can apply any [SoX effect](http://sox.sourceforge.net/sox.html#EFFECTS) to the audio while playing it


## Installation

Google Speech needs Python >= 3.4. It probably works with Python 3.3 with minimum efforts, or even previous 3.x versions, but I have not tested it.

1. Clone this repository
2. If you don't have it, [install pip](http://www.pip-installer.org/en/latest/installing.html) for Python3 (may not be needed with Python >= 3.4).
On Ubuntu and other Debian derivatives, you can install with `sudo apt-get install python3-pip`
3. Install Python dependencies: `pip3 install -r requirements.txt`
4. Install [SoX](http://sox.sourceforge.net/), with MP3 support.
On Ubuntu and other Debian derivatives: `sudo apt-get install sox libsox-fmt-mp3`.
Windows users can [download binaries on the SoX website](http://sourceforge.net/projects/sox/files/sox/), once installed you also need to add sox `play` executable directory to your PATH.


## Command line usage

Run `./google_speech.py -h` to get full command line reference.


## Examples

* Plane stall alarm:

    `./google_speech.py -l en stall -e delay 0.5 overdrive 20 repeat 5 speed 0.9 gain -5`

* Female robot voice (idea from [here](http://ubuntuforums.org/showthread.php?t=1813001&p=11090789#post11090789)):

    `./google_speech.py -l en "Hello, I am a stupid robot voice" -e speed 0.9 overdrive 10 echo 0.8 0.7 6 0.7 echo 0.8 0.7 10 0.7 echo 0.8 0.7 12 0.7 echo 0.8 0.88 12 0.7 echo 0.8 0.88 30 0.7 echo 0.6 0.6 60 0.7`

On Unix systems, with Bash and pipes, you can be creative:

* Bash greetings:

    `./google_speech.py -l en "Hello $USER, it is $(date)"`

* Countdown:

    `for i in {10..0}; do ( ./google_speech.py $i & ); sleep 1s; done`

* Read a Chuck Norris joke:

    `curl -s http://api.icndb.com/jokes/random/ | python3 -c 'import sys, json, xml.sax.saxutils; print(xml.sax.saxutils.unescape(json.load(sys.stdin)["value"]["joke"]))' | ./google_speech.py -`


## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0-standalone.html)
