from collections import namedtuple

from conceptgraphs import Graph as CG

from modules.tag_extract import tag_extract

Metrics = namedtuple('Metrics', ['precision', 'recall', 'f'])

def concept_coverage (graph, text, tags={'N','V','J','R'}):
    text_concepts = CG(grammar=tag_extract(tags), text=text).all_concepts()
    graph_concepts = graph.all_concepts()

    overlap = len(graph_concepts & text_concepts)
    prec = overlap / len(graph_concepts)
    recall = overlap / len(text_concepts)
    f = 2*recall*prec/(recall+prec)
    return Metrics(prec,recall,f)
