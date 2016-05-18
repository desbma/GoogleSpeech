#!/usr/bin/env python3

""" Read a text using Google Translate TTS API. """

__version__ = "1.0.15"
__author__ = "desbma"
__license__ = "GPLv3"

import argparse
import collections
import itertools
import logging
import os
import re
import subprocess
import string
import sys
import threading
import urllib.parse

import appdirs
import requests

from google_speech import bin_dep
from google_speech import colored_logging
from google_speech import web_cache


SUPPORTED_LANGUAGES = ("af", "ar", "az", "be", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en", "eo", "es", "et",
                       "eu", "fa", "fi", "fr", "ga", "gl", "gu", "hi", "hr", "ht", "hu", "id", "is", "it", "iw", "ja",
                       "ka", "kn", "ko", "la", "lt", "lv", "mk", "ms", "mt", "nl", "no", "pl", "pt", "ro", "ru", "sk",
                       "sl", "sq", "sr", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "vi", "yi", "zh-CN",
                       "zh-TW")

PRELOADER_THREAD_COUNT = 1


class PreloaderThread(threading.Thread):

  """ Thread to pre load (download and store in cache) audio data of a segment. """

  def run(self):
    try:
      for segment in self.segments:
        acquired = segment.preload_mutex.acquire(blocking=False)
        if acquired:
          try:
            if not segment.isInCache():
              segment.preLoad()
          finally:
            segment.preload_mutex.release()
    except Exception as e:
      logging.getLogger().error("%s: %s" % (e.__class__.__qualname__, e))


class Speech:

  """ Text to be read. """

  CLEAN_MULTIPLE_SPACES_REGEX = re.compile("\s{2,}")
  MAX_SEGMENT_SIZE = 100

  def __init__(self, text, lang):
    self.text = self.cleanSpaces(text)
    self.lang = lang

  def __iter__(self):
    """ Get an iterator over speech segments. """
    return self.__next__()

  def __next__(self):
    """ Get a speech segment, splitting text by taking into account spaces, punctuation, and maximum segment size. """
    if self.text == "-":
      if sys.stdin.isatty():
        logging.getLogger().error("Stdin is not a pipe")
        return
      while True:
        new_line = sys.stdin.readline()
        if not new_line:
          return
        segments = __class__.splitText(new_line)
        for segment_num, segment in enumerate(segments):
          yield SpeechSegment(segment, self.lang, segment_num, len(segments))

    else:
      segments = __class__.splitText(self.text)
      for segment_num, segment in enumerate(segments):
        yield SpeechSegment(segment, self.lang, segment_num, len(segments))

  @staticmethod
  def splitText(text):
    useless_chars = frozenset(string.punctuation + string.whitespace)
    segments = []
    left = __class__.cleanSpaces(text)
    previous_right = None
    while True:
      while len(left) > __class__.MAX_SEGMENT_SIZE:
        lr = tuple(map(__class__.cleanSpaces, left.rsplit(" ", 1)))
        if len(lr) == 2:
          left, right = lr
        else:
          left = lr[0][:__class__.MAX_SEGMENT_SIZE]
          right = lr[0][__class__.MAX_SEGMENT_SIZE:]
        if previous_right is not None:
          previous_right = "%s %s" % (right, previous_right)
        else:
          previous_right = right
      if any(itertools.filterfalse(useless_chars.__contains__, left)):
        segments.append(left)
      if not previous_right:
        break
      left = previous_right
      previous_right = None
    return segments

  @staticmethod
  def cleanSpaces(dirty_string):
    """ Remove consecutive spaces from a string. """
    return __class__.CLEAN_MULTIPLE_SPACES_REGEX.sub(" ",
                                                     dirty_string.replace("\n", " ").replace("\t", " ").strip())

  def play(self, sox_effects):
    """ Play a speech. """
    if self.text != "-":
      segments = list(self)
      # start preloader thread(s)
      preloader_threads = [PreloaderThread(name="PreloaderThread-%u" % (i)) for i in range(PRELOADER_THREAD_COUNT)]
      for preloader_thread in preloader_threads:
        preloader_thread.segments = segments
        preloader_thread.start()
    else:
      segments = iter(self)

    # play segments
    for segment in segments:
      segment.play(sox_effects)

    if self.text != "-":
      # destroy preloader threads
      for preloader_thread in preloader_threads:
        preloader_thread.join()


class SpeechSegment:

  """ Text segment to be read. """

  BASE_URL = "https://translate.google.com/translate_tts"

  session = requests.Session()

  def __init__(self, text, lang, segment_num, segment_count=None):
    self.text = text
    self.lang = lang
    self.segment_num = segment_num
    self.segment_count = segment_count
    self.preload_mutex = threading.Lock()
    if not hasattr(__class__, "cache"):
      db_filepath = os.path.join(appdirs.user_cache_dir(appname="google_speech",
                                                        appauthor=False),
                                 "google_speech-cache.sqlite")
      os.makedirs(os.path.dirname(db_filepath), exist_ok=True)
      cache_name = "sound_data"
      __class__.cache = web_cache.ThreadedWebCache(db_filepath,
                                                   cache_name,
                                                   expiration=60 * 60 * 24 * 365,  # 1 year
                                                   caching_strategy=web_cache.CachingStrategy.LRU)
      logging.getLogger().debug("Total size of file '%s': %s" % (db_filepath,
                                                                 __class__.cache.getDatabaseFileSize()))
      purged_count = __class__.cache.purge()
      logging.getLogger().debug("%u obsolete entries have been removed from cache '%s'" % (purged_count, cache_name))
      row_count = len(__class__.cache)
      logging.getLogger().debug("Cache '%s' contains %u entries" % (cache_name, row_count))

  def __str__(self):
    return self.text

  def isInCache(self):
    """ Return True if audio data for this segment is present in cache, False otherwise. """
    url = self.buildUrl(cache_friendly=True)
    return url in __class__.cache

  def preLoad(self):
    """ Store audio data in cache for fast playback. """
    logging.getLogger().debug("Preloading segment '%s'" % (self))
    real_url = self.buildUrl()
    cache_url = self.buildUrl(cache_friendly=True)
    audio_data = self.download(real_url)
    assert(audio_data)
    __class__.cache[cache_url] = audio_data

  def play(self, sox_effects):
    """ Play the segment. """
    with self.preload_mutex:
      cache_url = self.buildUrl(cache_friendly=True)
      if cache_url in __class__.cache:
        logging.getLogger().debug("Got data for URL '%s' from cache" % (cache_url))
        audio_data = __class__.cache[cache_url]
        assert(audio_data)
      else:
        real_url = self.buildUrl()
        audio_data = self.download(real_url)
        assert(audio_data)
        __class__.cache[cache_url] = audio_data
    logging.getLogger().info("Playing speech segment (%s): '%s'" % (self.lang, self))
    cmd = ["sox", "-q", "-t", "mp3", "-"]
    if sys.platform.startswith("win32"):
      cmd.extend(("-t", "waveaudio"))
    cmd.extend(("-d", "trim", "0.1", "reverse", "trim", "0.07", "reverse"))  # "trim", "0.25", "-0.1"
    if sox_effects is not None:
      cmd.extend(sox_effects)
    logging.getLogger().debug("Start player process")
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.DEVNULL)
    p.communicate(input=audio_data)
    if p.returncode != 0:
      raise RuntimeError()
    logging.getLogger().debug("Done playing")

  def buildUrl(self, cache_friendly=False):
    """
    Construct the URL to get the sound from Goggle API.

    If cache_friendly is True, remove token from URL to use as a cache key.
    """
    params = collections.OrderedDict()
    params["client"] = "tw-ob"
    params["ie"] = "UTF-8"
    params["idx"] = str(self.segment_num)
    if self.segment_count is not None:
      params["total"] = str(self.segment_count)
    params["textlen"] = str(len(self.text))
    params["tl"] = self.lang
    lower_text = self.text.lower()
    params["q"] = lower_text
    return "%s?%s" % (__class__.BASE_URL, urllib.parse.urlencode(params))

  def download(self, url):
    """ Download a sound file. """
    logging.getLogger().debug("Downloading '%s'..." % (url))
    response = __class__.session.get(url,
                                     headers={"User-Agent": "Mozilla/5.0"},
                                     timeout=3.1)
    response.raise_for_status()
    return response.content


def main(text, lang, sox_effects):
  # play
  Speech(text, lang).play(sox_effects)


def cl_main():
  # parse args
  arg_parser = argparse.ArgumentParser(description="Google Speech v%s.%s" % (__version__, __doc__),
                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  arg_parser.add_argument("speech",
                          help="Text to play")
  arg_parser.add_argument("-l",
                          "--lang",
                          choices=SUPPORTED_LANGUAGES,
                          default="en",
                          dest="lang",
                          help="Language")
  arg_parser.add_argument("-e",
                          "--sox-effects",
                          default=None,
                          nargs="+",
                          dest="sox_effects",
                          help="SoX effect command to pass to SoX's play")
  arg_parser.add_argument("-v",
                          "--verbosity",
                          choices=("warning", "normal", "debug"),
                          default="normal",
                          dest="verbosity",
                          help="Level of logging output")
  args = arg_parser.parse_args()

  # setup logger
  logging_level = {"warning": logging.WARNING,
                   "normal": logging.INFO,
                   "debug": logging.DEBUG}
  logging.getLogger().setLevel(logging_level[args.verbosity])
  logging.getLogger("requests").setLevel(logging.ERROR)
  logging.getLogger("urllib3").setLevel(logging.ERROR)
  if logging_level[args.verbosity] == logging.DEBUG:
    fmt = "%(asctime)s %(threadName)s: %(message)s"
  else:
    fmt = "%(message)s"
  logging_formatter = colored_logging.ColoredFormatter(fmt=fmt)
  logging_handler = logging.StreamHandler()
  logging_handler.setFormatter(logging_formatter)
  logging.getLogger().addHandler(logging_handler)

  # main
  main(args.speech, args.lang, args.sox_effects)


# check deps
bin_dep.check_bin_dependency(("sox",))


if __name__ == "__main__":
  cl_main()
