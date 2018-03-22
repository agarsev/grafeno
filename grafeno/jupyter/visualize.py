from IPython.display import HTML
import json

import os
path = os.path.dirname(__file__)

with open(os.path.join(path, 'app.js'), 'r') as file:
    app_js = file.read()

with open(os.path.join(path, 'app.html'), 'r') as file:
    app_html = file.read()

def visualize (graph):
    '''Make an interactive output cell with the graph data.'''

    nodes = graph.nodes()
    links = [{'source': u, 'target': v, **data}
             for u, v, data in graph.all_edges()]

    return HTML(app_html
        +'<script>'
        +"var graph = JSON.parse('{}')\n".format(
            json.dumps({'nodes': nodes, 'links': links}))
        +app_js
        +'</script>')


