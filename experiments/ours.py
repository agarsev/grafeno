from modules.deep_grammar import Transformer as Deep
from modules.sentence_record import Transformer as SentRecord
from modules.extend import Transformer as Extend
from modules.similarity_link import Transformer as SimLink

class Transformer (SimLink, Extend, Deep, SentRecord):
    pass
