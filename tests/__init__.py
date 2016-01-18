#!/usr/bin/env python3

import itertools
import logging
import socket
import sys
import tempfile
import unittest

import google_speech
from . import web_cache_test


google_speech.web_cache.DISABLE_PERSISTENT_CACHING = True


def is_internet_reachable():
  try:
    # open TCP socket to Google DNS server
    with socket.create_connection(("8.8.8.8", 53)):
      pass
  except OSError as e:
    if e.errno == 101:
      return False
    raise
  return True


class TestGoogleSpeech(unittest.TestCase):

  @unittest.skipUnless(is_internet_reachable(), "Need Internet access")
  def test_speechLoremIpsum(self):
    """ Play some reference speeches. """
    speeches = ("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
                "Le Lorem Ipsum est simplement du faux texte employé dans la composition et la mise en page avant impression. Le Lorem Ipsum est le faux texte standard de l'imprimerie depuis les années 1500, quand un peintre anonyme assembla ensemble des morceaux de texte pour réaliser un livre spécimen de polices de texte.")
    for lang, speech in zip(("en", "fr"), speeches):
      for effect in (None, ("speed", "10")):
        google_speech.main(speech, lang, effect)

  def test_splitTest(self):
    """ Split input text. """
    text = "Aaaa, bbbb. Cccc, dddd. %s. %s, %s. %s? %s ! %s, %s %s." % ("e" * (google_speech.Speech.MAX_SEGMENT_SIZE + 10),
                                                                        "f" * (google_speech.Speech.MAX_SEGMENT_SIZE - 1),
                                                                        "g" * (google_speech.Speech.MAX_SEGMENT_SIZE),
                                                                        "h" * (google_speech.Speech.MAX_SEGMENT_SIZE),
                                                                        "i" * (google_speech.Speech.MAX_SEGMENT_SIZE),
                                                                        "j" * (google_speech.Speech.MAX_SEGMENT_SIZE + 1),
                                                                        "k" * google_speech.Speech.MAX_SEGMENT_SIZE,
                                                                        "l" * 5)
    split_text = ("Aaaa, bbbb. Cccc, dddd.",
                  "%s" % ("e" * google_speech.Speech.MAX_SEGMENT_SIZE),
                  "%s." % ("e" * 10),
                  "%s," % ("f" * (google_speech.Speech.MAX_SEGMENT_SIZE - 1)),
                  "%s" % ("g" * google_speech.Speech.MAX_SEGMENT_SIZE),
                  "h" * google_speech.Speech.MAX_SEGMENT_SIZE,
                  "i" * google_speech.Speech.MAX_SEGMENT_SIZE,
                  "j" * google_speech.Speech.MAX_SEGMENT_SIZE,
                  "j,",
                  "k" * google_speech.Speech.MAX_SEGMENT_SIZE,
                  "lllll.")

    # input is text string
    speech = google_speech.Speech(text, "en")
    for segment, ref_text in itertools.zip_longest(speech, split_text):
      self.assertEqual(segment.text, ref_text)

    # input is stdin
    with tempfile.SpooledTemporaryFile(mode="w+t") as text_file:
      for i in range(3):
        text_file.write(text)
        text_file.write("\n")
      text_file.seek(0)
      original_stdin, sys.stdin = sys.stdin, text_file
      speech = google_speech.Speech("-", "fr")
      for i, (segment, ref_text) in enumerate(zip(speech, itertools.cycle(split_text)), 1):
        self.assertEqual(segment.text, ref_text)
      self.assertEqual(i, len(split_text * 3))
      sys.stdin = original_stdin


if __name__ == "__main__":
  # disable logging
  logging.basicConfig(level=logging.CRITICAL + 1)

  # run tests
  unittest.main()
