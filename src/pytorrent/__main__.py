import logging
import sys

from .main import Run

logging.basicConfig(level=logging.DEBUG)

try:
  torrent_file = sys.argv[1]
except IndexError:
  logging.error("No torrent file provided!")
  sys.exit(1)

run = Run(torrent_file)
run.start()
