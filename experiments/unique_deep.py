from modules.deep_grammar import Transformer as Deep
from modules.sentence_record import Transformer as SentRecord
from modules.extend import Transformer as Extend
from modules.similarity_link import Transformer as SimLink
from modules.unique_nodes import Transformer as Uniq

class Transformer (SimLink, Extend, Uniq, Deep, SentRecord):
    pass
