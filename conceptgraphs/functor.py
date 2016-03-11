from enum import Enum

class Functor(Enum):

    AGENT = 1
    THEME = 2
    ADV = 3
    ATTR = 4
    JUX = 5

    def is_semantic(self):
        return self.value in {1, 2, 3, 4}

    def is_discourse(self):
        return self.value in {5,}