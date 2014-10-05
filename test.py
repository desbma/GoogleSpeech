import inspect
import os
import random
import socket
import string
import sys


def add_script_import_dir(dir):
  script_dir = os.path.dirname(os.path.dirname(inspect.getfile(inspect.currentframe())))
  needed_import_dir = os.path.join(script_dir, dir)
  if needed_import_dir not in sys.path:
    sys.path.insert(0, needed_import_dir)


def get_random_string(length, chars=string.ascii_letters + string.digits):
  return "".join(random.choice(chars) for _ in range(length))


def is_internet_reachable():
  try:
    # open TCP socket to Google DNS server
    socket.create_connection(("8.8.8.8", 53))
  except OSError as e:
    if e.errno == 101:
      return False
    raise
  return True
