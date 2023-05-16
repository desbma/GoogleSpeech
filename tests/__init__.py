#!/usr/bin/env python3

import itertools
import logging
import os
import socket
import sys
import tempfile
import unittest

import google_speech


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

  def setUp(self):
    self.orig_audiodev = os.environ.get("AUDIODEV")
    os.environ["AUDIODEV"] = "null"

  def tearDown(self):
    if self.orig_audiodev is not None:
      os.environ["AUDIODEV"] = self.orig_audiodev
    else:
      del os.environ["AUDIODEV"]

  @unittest.skipUnless(is_internet_reachable(), "Need Internet access")
  def test_speechLoremIpsum(self):
    """ Play some reference speeches. """
    speeches = ("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
                "Le Lorem Ipsum est simplement du faux texte employé dans la composition et la mise en page avant impression. Le Lorem Ipsum est le faux texte standard de l'imprimerie depuis les années 1500, quand un peintre anonyme assembla ensemble des morceaux de texte pour réaliser un livre spécimen de polices de texte.")
    for lang, speech in zip(("en", "fr"), speeches):
      for effect in ((), ("speed", "10")):
        max_segment_size: int = 100
        google_speech.Speech(speech, lang, max_segment_size).play(effect)

  def test_splitTest(self):
    max_segment_size: int = 100

    """ Split input text. """
    text = ("Aaaa, bbbb. Cccc, dddd. "
            "%s. %s, %s. %s? %s ! %s, %s %s. %s, %s %s" % ("e" * (max_segment_size + 10),
                                                           "f" * (max_segment_size - 1),
                                                           "g" * (max_segment_size),
                                                           "h" * (max_segment_size),
                                                           "i" * (max_segment_size),
                                                           "j" * (max_segment_size + 1),
                                                           "k" * max_segment_size,
                                                           "l" * 5,
                                                           "m" * (max_segment_size - 20),
                                                           "n" * 10,
                                                           "o" * 15))
    split_text = ("Aaaa, bbbb. Cccc, dddd.",
                  "%s" % ("e" * max_segment_size),
                  "%s." % ("e" * 10),
                  "%s," % ("f" * (max_segment_size - 1)),
                  "%s" % ("g" * max_segment_size),
                  "h" * max_segment_size,
                  "i" * max_segment_size,
                  "j" * max_segment_size,
                  "j,",
                  "k" * max_segment_size,
                  "lllll. %s," % ("m" * (max_segment_size - 20)),
                  "%s %s" % ("n" * 10, "o" * 15))

    # input is text string
    speech = google_speech.Speech(text, "en", max_segment_size)
    for segment, ref_text in itertools.zip_longest(speech, split_text):
      self.assertEqual(segment.text, ref_text)

    # input is stdin
    with tempfile.SpooledTemporaryFile(mode="w+t") as text_file:
      for i in range(3):
        text_file.write(text)
        text_file.write("\n")
      text_file.seek(0)
      original_stdin, sys.stdin = sys.stdin, text_file
      speech = google_speech.Speech("-", "fr", max_segment_size)
      for i, (segment, ref_text) in enumerate(zip(speech, itertools.cycle(split_text)), 1):
        self.assertEqual(segment.text, ref_text)
      self.assertEqual(i, len(split_text * 3))
      sys.stdin = original_stdin


class TestValidaters(unittest.TestCase):
    def test_check_positive(self):
        import argparse
        for s in ["-1", "0", "1.0", "-1.0", ".0", "1.", "hello"]:
            self.assertRaisesRegex(argparse.ArgumentTypeError, f'^{s} is an invalid positive int value$', google_speech.check_positive, s)
        for s in ["1", "2"]:
            try:
                google_speech.check_positive(s)
            except:
                self.fail("`check_positive() raised an exception unexpectedly")


if __name__ == "__main__":
  # disable logging
  logging.basicConfig(level=logging.CRITICAL + 1)

  # run tests
  unittest.main()
