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


## Examples

Bash greetings: `./google_speech.py "Hello $USER, it is $(date)"`

Plane stall alarm: `./google_speech.py -l en stall -e delay 0.5 overdrive 20 repeat 5 speed 0.9 gain -5`

Female robot voice (idea from [here](http://ubuntuforums.org/showthread.php?t=1813001&p=11090789#post11090789)): `./google_speech.py -l en "Hello, I am a stupid robot voice" -e speed 0.9 overdrive 10 echo 0.8 0.7 6 0.7 echo 0.8 0.7 10 0.7 echo 0.8 0.7 12 0.7 echo 0.8 0.88 12 0.7 echo 0.8 0.88 30 0.7 echo 0.6 0.6 60 0.7`

Read a Chuck Norris joke: `curl -s http://api.icndb.com/jokes/random/ | python3 -c 'import sys, json, xml.sax.saxutils; print(xml.sax.saxutils.unescape(json.load(sys.stdin)["value"]["joke"]))' | ./google_speech.py -`


## Command line reference

    usage: google_speech.py [-h]
                            [-l {af,ar,az,be,bg,bn,ca,cs,cy,da,de,el,en,eo,es,et,eu,fa,fi,fr,ga,gl,gu,hi,hr,ht,hu,id,is,it,iw,ja,ka,kn,ko,la,lt,lv,mk,ms,mt,nl,no,pl,pt,ro,ru,sk,sl,sq,sr,sv,sw,ta,te,th,tl,tr,uk,ur,vi,yi,zh-CN,zh-TW}]
                            [-e SOX_EFFECTS [SOX_EFFECTS ...]]
                            [-v {warning,normal,debug}]
                            speech

    Read a text using Google API.

    positional arguments:
      speech                Text to play

    optional arguments:
      -h, --help            show this help message and exit
      -l {af,ar,az,be,bg,bn,ca,cs,cy,da,de,el,en,eo,es,et,eu,fa,fi,fr,ga,gl,gu,hi,hr,ht,hu,id,is,it,iw,ja,ka,kn,ko,la,lt,lv,mk,ms,mt,nl,no,pl,pt,ro,ru,sk,sl,sq,sr,sv,sw,ta,te,th,tl,tr,uk,ur,vi,yi,zh-CN,zh-TW}, --lang {af,ar,az,be,bg,bn,ca,cs,cy,da,de,el,en,eo,es,et,eu,fa,fi,fr,ga,gl,gu,hi,hr,ht,hu,id,is,it,iw,ja,ka,kn,ko,la,lt,lv,mk,ms,mt,nl,no,pl,pt,ro,ru,sk,sl,sq,sr,sv,sw,ta,te,th,tl,tr,uk,ur,vi,yi,zh-CN,zh-TW}
                            Language
      -e SOX_EFFECTS [SOX_EFFECTS ...], --sox-effects SOX_EFFECTS [SOX_EFFECTS ...]
                            SoX effect command to pass to SoX's play
      -v {warning,normal,debug}, --verbosity {warning,normal,debug}
                            Level of output to display


## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0-standalone.html)
