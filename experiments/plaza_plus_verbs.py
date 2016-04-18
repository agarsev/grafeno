from modules.pos_extract import Transformer as PosExtract
from modules.sentence_record import Transformer as SentRecord
from modules.extend import Transformer as Extend
from modules.similarity_link import Transformer as SimLink
from modules.unique_nodes import Transformer as Uniq

class Transformer (SimLink, Extend, Uniq, SentRecord, PosExtract):

    def __init__ (self, **kwds):
        super().__init__(sempos={'noun':'v'}, **kwds)
