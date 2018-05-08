from IPython.display import display, HTML, Javascript
import json

import os
path = os.path.dirname(__file__)

with open(os.path.join(path, 'app.js'), 'r') as file:
    app_js = file.read()
    display(Javascript(app_js))

with open(os.path.join(path, 'app.html'), 'r') as file:
    app_html = file.read()

output_counter = 1

def visualize (graph):
    '''Make an interactive output cell with the graph data.'''

    global output_counter
    output_counter += 1

    nodes = graph.nodes()
    links = [{'source': u, 'target': v, **data}
             for u, v, data in graph.all_edges()]

    return HTML(app_html.replace("$OUTPUT_COUNTER$", str(output_counter))
        +"<script>CreateGrafenoVisualization({},JSON.parse('{}'))</script>"
        .format(output_counter, json.dumps({'nodes': nodes, 'links': links}))
        )


