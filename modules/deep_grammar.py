from .pos_extract import Grammar as PosExtract

class Grammar (PosExtract):

    predication = {
            'ncsubj': 'AGENT',
            'dobj': 'THEME',
            'iobj': 'IOBJ'
            }

    def __init__ (self):
        super().__init__()

    def transform_node (self, msnode):
        sem = super().transform_node(msnode)
        sempos = sem.get('sempos')
        if sem.get('concept') == 'be' and not msnode:
            del sem['concept']
            sem['copula'] = True
        elif sempos == 'n':
            sem['proper'] = msnode.get('type') == 'proper'
            sem['num'] = msnode.get('num','p')
        elif sempos == 'v':
            sem['tense'] = msnode.get('vform')
        elif msnode.get('pos') == 'preposition':
            sem['pval'] = msnode.get('lemma')
        return sem

    def transform_dep (self, dep, parent, child):
        edge = super().transform_dep(dep, parent, child)
        if self.copula(dep, parent, child, edge) or \
           self.prep_rising(dep, parent, child, edge):
                pass
        elif 'concept' not in parent or 'concept' not in child:
            return edge
        elif parent.get('sempos') == 'v' and dep in self.predication:
            edge['functor'] = self.predication[dep]
        elif dep == 'ncmod':
            edge['functor'] = 'ATTR'
        return edge

    def copula (self, dep, parent, child, edge):
        if parent.get('concept') != 'be':
            return False
        if dep == 'ncsubj':
            parent['copula_s'] = edge['child']
        else:
            parent['coputa_a'] = edge['child']
        if 'copula_s' in parent and 'copula_a' in parent:
            edge['functor'] = 'ATTR'
            edge['parent'] = parent['copula_s']
            edge['child'] = parent['copula_a']
            del parent['concept']
        return True

    def prep_rising (self, dep, parent, child, edge):
        if 'pval' not in parent and 'pval' not in child:
            return False
        if 'pval' in parent:
            parent['prep_obj'] = edge['child']
            prep_node = parent
        if 'pval' in child:
            child['prep_parent'] = edge['parent']
            prep_node = child
        if 'prep_obj' in prep_node and 'prep_parent' in prep_node:
            edge['functor'] = 'COMP'
            edge['gram']['pval'] = prep_node['pval']
            edge['parent'] = prep_node['prep_parent']
            edge['child'] = prep_node['prep_obj']
            del prep_node['pval']
        return True
