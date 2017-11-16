import atexit
from py4j_server import launch_py4j_server
from py4j.java_gateway import java_import

jvm = None

def init_gateway ():
    global jvm
    if not jvm:
        gateway = launch_py4j_server()
        jvm = gateway.jvm
        java_import(jvm, "simplenlg.features.*")
        java_import(jvm, "simplenlg.realiser.*")
        atexit.register(gateway.close)

class Linearizer ():

    def __init__ (self, graph=None, **kwds):
        self.graph=graph
        init_gateway()

    def linearize (self):
        phrases = [ self.process_node(v)
                   for v in self.graph.nodes()
                   if v.get('sempos')=='v' ]
        return ' '.join(phrases).strip()

    def process_node (self, node):
        sempos = node['sempos']
        if sempos == 'n':
            return self.process_noun(node)
        elif sempos == 'v':
            return self.process_verb(node)
        else:
            return self.process_other(node)

    def process_verb (self, verb):
        phrase = jvm.SPhraseSpec()
        concept = verb.get('concept').replace('_', ' ')
        phrase.setVerb(concept)
        for node, edge in self.graph.neighbours(verb):
            child = self.process_node(node)
            self.process_edge(phrase, child, edge)
        phrase.setInterrogative(jvm.InterrogativeType.YES_NO)
        phrase.setTense(jvm.Tense.PAST)
        realiser = jvm.Realiser()
        return realiser.realiseDocument(phrase)

    def process_noun (self, node):
        np = jvm.NPPhraseSpec(node.get('concept'))
        for mod, edge in self.graph.neighbours(node):
            child = self.process_node(mod)
            self.process_edge(np, child, edge)
        return np

    def process_other (self, node):
        return node.get('concept')

    def process_edge (self, parent, child, edge):
        if edge['functor'] == 'AGENT':
            parent.addSubject(child)
        elif edge['functor'] == 'COMP':
            prep = jvm.PPPhraseSpec()
            prep.setPreposition(edge.get('pval'))
            prep.addComplement(child)
            parent.addModifier(prep)
        elif edge['functor'] == 'ATTR':
            parent.addModifier(child)
        else:
            parent.addComplement(child)
