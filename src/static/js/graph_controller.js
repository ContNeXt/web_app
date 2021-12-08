$(document).ready(function () {

    // render network
    initD3Force(graphData);

    // Controls behaviour of clicking in dropdowns
    $('li.dropdown.mega-dropdown a').on('click', function () {
        $(this).parent().toggleClass('open');
    });

    $('body').on('click', function (e) {
        if (!$('li.dropdown.mega-dropdown').is(e.target)
            && $('li.dropdown.mega-dropdown').has(e.target).length === 0
            && $('.open').has(e.target).length === 0
        ) {
            $('li.dropdown.mega-dropdown').removeClass('open');
        }
    });
});

/**
 * Initialize d3 Force to plot network from json
 * @param {object} graph json data
 */

d3.json("/api/explorer/{node}/{network_id}", function initD3Force(graph) {

    //////////////////////////////
    // Main graph visualization //
    //////////////////////////////

    $(".disabled").attr("class", "nav-link ");     // Enable nodes and edges tabs

    var graphDiv = $("#graph-chart"); // Force div

    var nodePanel = $("#node-list"); // Node submit_data div

    var edgePanel = $("#edge-list"); // Edge submit_data div

    d = document;
    e = d.documentElement;
    g = d.getElementsByTagName("body")[0];

    var w = graphDiv.width(), h = graphDiv.height();

    // Simulation parameters
    var linkDistance = 100, fCharge = -1700, linkStrength = 0.7, collideStrength = 1;

    // Simulation defined with variables
    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink()
            .distance(linkDistance)
            .strength(linkStrength)
        )
        .force("collide", d3.forceCollide()
            .radius(function (d) {
                return d.r + 10
            })
            .strength(collideStrength)
        )
        .force("charge", d3.forceManyBodyReuse()
            .strength(fCharge)
        )
        .force("center", d3.forceCenter(w / 2, h / 2))
        .force("y", d3.forceY(0))
        .force("x", d3.forceX(0));

    // Pin down functionality
    var nodeDrag = d3.drag()
        .on("start", dragStarted)
        .on("drag", dragged)
        .on("end", dragEnded);

    // Methods to drug the groups (convex hulls)
    function groupDragStarted() {
        if (!d3.event.active) simulation.alphaTarget(simulationAlpha).restart();
        d3.select(this).select('path').style('stroke-width', 3);
    }

    function groupDragged(subgraphGroup) {
        $.each(getNodesInSubgraph(subgraphGroup, graph.links), function (index, d) {
            d.x += d3.event.dx;
            d.y += d3.event.dy;
        });
    }

    function groupDragEnded() {
        if (!d3.event.active) simulation.alphaTarget(simulationAlpha).restart();
        d3.select(this).select('path').style('stroke-width', 1);
    }

    function dragStarted(d) {
        if (!d3.event.active) simulation.alphaTarget(simulationAlpha).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragEnded() {
        if (!d3.event.active) simulation.alphaTarget(0);
    }

    function releaseNode(d) {
        d.fx = null;
        d.fy = null;
    }

    //END Pin down functionality

    var svg = d3.select("#graph-chart").append("svg")
        .attr("class", "svg-border")
        .attr("id", "graph-svg")
        .attr("width", w)
        .attr("height", h);

    // // Create definition for arrowhead.
    svg.append("defs").append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 20)
        .attr("refY", 0)
        .attr("markerUnits", "strokeWidth")
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .attr("opacity", opacity)
        .append("path")
        .attr("d", "M0,-5L10,0L0,5");

    // // Create definition for stub.
    svg.append("defs").append("marker")
        .attr("id", "stub")
        .attr("viewBox", "-1 -5 2 10")
        .attr("refX", 15)
        .attr("refY", 0)
        .attr("markerUnits", "strokeWidth")
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .attr("opacity", opacity)
        .append("path")
        .attr("d", "M 0,0 m -1,-5 L 1,-5 L 1,5 L -1,5 Z");

    // // Create definition for cross.
    svg.append("defs").append("marker")
        .attr("id", "cross")
        .attr("viewBox", "-1 -5 2 10")
        .attr("refX", 15)
        .attr("refY", 0)
        .attr("markerUnits", "strokeWidth")
        .attr("markerWidth", 2)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .attr("opacity", opacity)
        .append("path")
        .attr("d", "M 3,3 L 7,7 M 3,7 L 7,3");


    // Background
    svg.append("rect")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("fill", "#fcfbfb")
        .style("pointer-events", "all");

    var g = svg.append("g");  // g = svg object where the graph will be appended

    var linkedByIndex = {};
    graph.links.forEach(function (d) {
        linkedByIndex[d.source + "," + d.target] = true;
    });

    function isConnected(a, b) {
        return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index === b.index;
    }

    function ticked() {
        link.attr("x1", function (d) {
            return d.source.x;
        })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node.attr("transform", function (d) {
            return "translate(" + d.x + ", " + d.y + ")";
        });

        if (hullsBoolean === true) {
            updateGroups(graph.links, paths);
        }
    }

    simulation.nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

});
