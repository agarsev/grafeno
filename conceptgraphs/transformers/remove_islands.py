from conceptgraphs.transformer import Transformer as Base

class Transformer (Base):

    def after_all (self):
        g = self.graph._g
        saved = set()
        for n in g:
            if len(g[n])!=0:
                saved.add(n)
                for m in g[n]:
                    saved.add(m)
        doomed = [n for n in g if n not in saved]
        for n in doomed:
            g.remove_node(n)
