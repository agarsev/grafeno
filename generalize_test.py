#!/usr/bin/env python3

from grafeno import Graph as CG, transformers as tr, linearizers as ln


T = tr.get_pipeline(['pos_extract','thematic','phrasal','wordnet'])
L = ln.get_pipeline(['simple_nlg'])

g1 = CG(transformer=T, text="A man picked up an apple.")
g2 = CG(transformer=T, text="The woman lifted some pears.")

import grafeno.operations.generalize as gen
g3 = gen.generalize(g1, g2, node_generalize=gen.wordnet_generalize)

print(g3.linearize(linearizer=L))
