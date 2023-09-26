# read version from installed package
from importlib.metadata import version
__version__ = version(__name__)
__author__ = 'alexisgallepe'
del version

from . import block
from . import main
from . import message
from . import peer
from . import peers_manager
from . import piece
from . import pieces_manager
from . import rarest_piece
from . import torrent
from . import tracker
