'use strict';

var m; // workaround for a weird minimizer problem

require.config({
    paths: {
        d3: '//cdnjs.cloudflare.com/ajax/libs/d3/3.4.8/d3.min'
    }
});

window.CreateGrafenoVisualization = function (output_counter, graph) {

    require(['d3'], function (d3) {
        function node_color(node) {
            switch (node.sempos) {
                case 'n':
                    return '#CF3C46';
                case 'v':
                    return '#44B033';
                case 'j':
                    return '#FBB136';
                case 'r':
                    return '#476FA5';
            }
        }
        function link_distance(link) {
            switch (link.functor) {
                case 'SEQ':
                    return 300;
                case 'ATTR':
                    return 80;
                default:
                    return 140;
            }
        }
        function middle_point(s, t) {
            var mx = (t.x + s.x) / 2,
                my = (t.y + s.y) / 2,
                dx = t.x - s.x,
                dy = t.y - s.y;
            return { x: mx + dy / 3,
                y: my - dx / 3
            };
        }
        var container = d3.select('#d3-container-' + output_counter).select("div");
        var _container$0$ = container[0][0],
            w = _container$0$.clientWidth,
            h = _container$0$.clientHeight;

        var zoom = d3.behavior.zoom().scaleExtent([.5, 5]).size([w, h]).translate([w / 2, h / 2]).on('zoom', zoomed);
        container.call(zoom);
        var force = d3.layout.force().charge(-300).gravity(0.05).linkDistance(link_distance);
        var svg = container.select("#graph-layer");
        function zoomed() {
            force.stop();
            var canvasTranslate = zoom.translate();
            svg.attr('transform', 'translate(' + canvasTranslate[0] + ',' + canvasTranslate[1] + ')scale(' + zoom.scale() + ')');
            force.resume();
        }
        zoomed();

        force.nodes(graph.nodes).links(graph.links).start();
        var link = svg.selectAll(".link").data(graph.links).enter().append("g").attr("class", "link");
        link.append("path");
        link.append("text").text(function (d) {
            return d.functor;
        });
        var node = svg.selectAll(".node").data(graph.nodes).enter().append("g").attr("class", "node");
        node.append("circle").attr("r", 30).style("fill", node_color).call(force.drag).on('mousedown', function () {
            return d3.event.stopPropagation();
        });
        node.append("text").text(function (d) {
            return d.concept;
        }).attr("dx", function (d) {
            return d.x;
        }).attr("dy", function (d) {
            return d.y;
        });
        node.append("title").text(function (d) {
            return d.concept;
        });
        force.on("tick", function () {
            link.select('path').attr("d", function (d) {
                var s = d.source,
                    t = d.target;
                m = middle_point(s, t);
                return 'M' + s.x + ',' + s.y + ' Q' + m.x + ',' + m.y + ' ' + t.x + ',' + t.y;
            });
            link.select('text').attr("dx", function (d) {
                return middle_point(d.source, d.target).x;
            }).attr("dy", function (d) {
                return middle_point(d.source, d.target).y;
            });
            node.select('circle').attr("cx", function (d) {
                return d.x;
            }).attr("cy", function (d) {
                return d.y;
            });
            node.select('text').attr("dx", function (d) {
                return d.x;
            }).attr("dy", function (d) {
                return d.y;
            });
        });
    });
};

/* vim: set filetype=javascript : */
