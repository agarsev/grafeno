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
    .linkDistance(link_distance);
var container = d3.select("#d3-container").select("div")
    .call(zoom);
var svg = container.select("#graph-layer");
function zoomed(){
    force.stop();
    var canvasTranslate = zoom.translate();
    svg.attr('transform', 'translate('+canvasTranslate[0]+','+canvasTranslate[1]+')scale(' + zoom.scale() + ')');
    force.resume();
}

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
});
