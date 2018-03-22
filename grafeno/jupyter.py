from IPython.display import display, HTML
import json

is_ready = False
display(HTML('<script src="http://d3js.org/d3.v3.min.js"></script>'))

def visualize (graph):
    '''Make an interactive output cell with the graph data.'''

    nodes = graph.nodes()
    links = [{'source': u, 'target': v, **data}
             for u, v, data in graph.all_edges()]

    return HTML('''
    <div id="d3-container"><svg>
        <defs>
          <marker id="markerArrow" markerWidth="6" markerHeight="8"
            orient="auto" refX="21" refY="3">
      <path d="M0,3 L6,5 1,8" />
    </marker>
        </defs>
        <g id="graph-layer"></g>
    </svg></div>
    <style>
    #d3-container { width: 700px; height: 500px; border: 1px solid black; }
    #d3-container svg { width: 100%; height: 100%; }
    .node circle {
        stroke: #fff;
        stroke-width: 2px;
    }
    .link path {
        stroke: #333; stroke-width: 2px;
        fill: none;
        marker-end: url(#markerArrow);
    }
    .link text, .node text {
        stroke: #fff;
        paint-order: stroke;
        stroke-width: 4px;
        fill: #333;
        text-anchor: middle;
        dominant-baseline: middle;
        font-weight: boldest;
        pointer-events: none;
    }
    .marker {
        fill: #333;
    }
    </style>
    <script>
    '''+
    "var graph = JSON.parse('{}')\n".format(
        json.dumps({'nodes': nodes, 'links': links}))
    +'''
    function node_color (node) {
        switch (node.sempos) {
            case 'n': return '#CF3C46';
            case 'v': return '#44B033';
            case 'j': return '#FBB136';
            case 'r': return '#476FA5';
        }
    }
    function link_distance (link) {
        switch (link.functor) {
            case 'SEQ':
                return 300;
            case 'ATTR':
                return 80;
            default:
                return 140;
        }
    }
    function middle_point (s, t) {
        var mx = (t.x + s.x)/2;
        var my = (t.y + s.y)/2;
        var dx = (t.x - s.x);
        var dy = (t.y - s.y);
        return { x: mx+dy/3,
                 y: my-dx/3
               };
    }
    var zoom = d3.behavior.zoom()
                    .scaleExtent([.5, 5])
                    .on('zoom', zoomed);
    var force = d3.layout.force()
        .charge(-200)
        .gravity(0.05)
        .linkDistance(link_distance)
        .size([700, 500]);
    var container = d3.select("#d3-container").select("svg")
        .call(zoom);
    var svg = container.select("#graph-layer");
    function zoomed(){
        force.stop();
        var canvasTranslate = zoom.translate();
        svg.attr('transform', 'translate('+canvasTranslate[0]+','+canvasTranslate[1]+')scale(' + zoom.scale() + ')');
        force.resume();
    }
    svg.selectAll("*").remove();

    force.nodes(graph.nodes)
        .links(graph.links)
        .start();
    var link = svg.selectAll(".link")
        .data(graph.links)
        .enter().append("g")
        .attr("class", "link");
    link.append("path");
    link.append("text")
        .text(function(d) { return d.functor; });
    var node = svg.selectAll(".node")
        .data(graph.nodes)
        .enter().append("g")
        .attr("class", "node");
    node.append("circle")
        .attr("r", 30)
        .style("fill", node_color)
        .call(force.drag)
        .on('mousedown', function(e){ d3.event.stopPropagation();});
    node.append("text")
        .text(function(d){return d.concept;})
        .attr("dx", function(d){return d.x;})
        .attr("dy", function(d){return d.y;});
    node.append("title")
        .text(function(d) { return d.concept; });
    force.on("tick", function() {
        link.select('path')
            .attr("d", function(d) {
                var s = d.source;
                var t = d.target;
                var m = middle_point(s, t);
                return "M"+s.x+","+s.y
                    +" Q"+m.x+","+m.y
                    +" "+t.x+","+t.y;
        });
        link.select('text')
            .attr("dx", function(d){return middle_point(d.source,d.target).x;})
            .attr("dy", function(d){return middle_point(d.source,d.target).y;});
        node.select('circle')
            .attr("cx", function(d){return d.x;})
            .attr("cy", function(d){return d.y;});
        node.select('text')
            .attr("dx", function(d){return d.x;})
            .attr("dy", function(d){return d.y;});
        setTimeout(function(){
            force.linkDistance(200);
        }, 5000)
    });
    ''')


