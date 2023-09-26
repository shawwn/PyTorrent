import unittest

from pytorrent import *
import os
import logging
import time

def path(to):
  return os.path.join(os.path.dirname(__file__), to)

class TestCase(unittest.TestCase):
  def test_basic(self):
    torrent_file = path("fixtures/test.torrent")
    self.torrent = torrent.Torrent().load_from_path(torrent_file)
    self.tracker = tracker.Tracker(self.torrent)
    self.pieces_manager = pieces_manager.PiecesManager(self.torrent)
    logging.info("PiecesManager Started")

    self.peers_manager = peers_manager.PeersManager(self.torrent, self.pieces_manager)
    self.peers_manager.start()
    logging.info("PeersManager Started")

    peers_dict = self.tracker.get_peers_from_trackers()
    self.peers_manager.add_peers(peers_dict.values())

    while not self.pieces_manager.all_pieces_completed():
      if not self.peers_manager.has_unchoked_peers():
        time.sleep(1)
        logging.info("No unchocked peers")
        continue

      for piece in self.pieces_manager.pieces:
        index = piece.piece_index

        if self.pieces_manager.pieces[index].is_full:
          continue

        peer = self.peers_manager.get_random_peer_having_piece(index)
        if not peer:
          continue

        self.pieces_manager.pieces[index].update_block_status()

        data = self.pieces_manager.pieces[index].get_empty_block()
        if not data:
          continue

        piece_index, block_offset, block_length = data
        piece_data = message.Request(piece_index, block_offset, block_length).to_bytes()
        peer.send_to_peer(piece_data)


    self.peers_manager.is_active = False
    self.peers_manager.join()
    logging.info("PeersManager Stopped")



if __name__ == '__main__':
  unittest.main()
