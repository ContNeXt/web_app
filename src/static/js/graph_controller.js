// Constants used in the graph controller
var nominalBaseNodeSize = 10; // Default node radius
var edgeStroke = 3.5;  // Edge width
var minZoom = 0.1, maxZoom = 30; // Zoom variables
var opacity = 0.3; //opacity links

//Convex Hull Constants
var polygon, groups;
var color = d3.scaleOrdinal(d3.schemeCategory10);
var simulationAlpha = 0.3; //Alpha simulation convex hulls


/**
 * Initialize d3 Force to plot network from json
 * @param {object} graph json data
 */
function initD3Force(graph) {

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
    }

    simulation.nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

    /////////////////////////////
    // Modify the simulation   //
    /////////////////////////////

    function inputted() {
        simulation.force("link").strength(+this.value);
        simulation.alpha(1).restart();
    }

    d3.select("#link-slider").on("input", inputted);

    ////////////////////////////////////////////////////
    // Definition of links, nodes, text, groups...
    ////////////////////////////////////////////////////

    groups = g.append('g').attr('class', 'groups');

    var link = g.selectAll(".link")
        .data(graph.links)
        .enter().append("line")
        .style("stroke-width", edgeStroke)
        .style("stroke-opacity", 0.4)

    var node = g.selectAll(".nodes")
        .data(graph.nodes)
        .enter().append("g")
        .attr("class", "node")
        // Next two lines -> Pin down functionality
        .on("dblclick", releaseNode)
        // Dragging
        .call(nodeDrag);

    var circle = node.append("circle")
        .attr("r", nominalBaseNodeSize)

    var text = node.append("text")
        .attr("class", "node-name")
        .attr("id", function (d) {
            return d.id;
        })
        .attr("fill", "black")
        .attr("dx", 16)
        .attr("dy", ".35em")
        .text(function (d) {
            return d.name;
        });

    // Highlight on mouse-enter and back to normal on mouseout
    node.on("mouseenter", function (data, index) {
        d3.select(this).classed('node_highlighted', true);


        link.classed("link_highlighted", function (o) {
            return o.source.index === index || o.target.index === index;
        });

        node.classed('node_highlighted', function (o) {
            return isConnected(data, o);
        });
    })
        .on("mousedown", function () {
            d3.event.stopPropagation();
        })
        .on("mouseout", function () {
            link.classed("link_highlighted", false);
            node.classed("node_highlighted", false);
        });


    // Highlight links on mouseenter and back to normal on mouseout
    link.on("mouseenter", function (data) {
        d3.select(this).classed('link_highlighted', true);
    })
        .on("mousedown", function () {
            d3.event.stopPropagation();
        })
        .on("mouseout", function () {
            d3.select(this).classed('link_highlighted', false);
        });


    /**
     * Freeze the graph when space is pressed
     */
    function freezeGraph() {
        if (d3.event.keyCode === 32) {
            simulation.stop();
        }
    }

    /**
     * Resets default styles for nodes/edges/text on double click
     */
    function resetAttributesDoubleClick() {
        // On double click reset attributes (Important disabling the zoom behavior of dbl click because it interferes with this)
        svg.on("dblclick", function () {
            // Remove the overriding stroke so the links default back to the CSS definitions
            link.style("stroke", null);

            // SET default attributes //
            svg.selectAll(".link, .node").style("visibility", "visible")
                .style("opacity", "1");
            // Show node names
            svg.selectAll(".node-name").style("visibility", "visible").style("opacity", "1");
        });

    }

    /**
     * Resets default styles for nodes/edges/text
     */
    function resetAttributes() {
        // Reset visibility and opacity
        svg.selectAll(".link, .node").style("visibility", "visible").style("opacity", "1");
        // Show node names
        svg.selectAll(".node-name").style("visibility", "visible").style("opacity", "1");
        svg.selectAll(".node-name").style("display", "block");
    }

    /**
     * Changes the opacity to 0.1 of edges that are not in array
     * @param {array} edgeArray
     * @param {string} property of the edge to filter
     */
    function highlightEdges(edgeArray, property) {
        // Array with names of the nodes in the selected edge
        var nodesInEdges = [];

        // Filtered not selected links
        var edgesNotInArray = g.selectAll(".link").filter(function (edgeObject) {

            if (edgeArray.indexOf(edgeObject.source[property] + "-" + edgeObject.target[property]) >= 0) {
                nodesInEdges.push(edgeObject.source[property]);
                nodesInEdges.push(edgeObject.target[property]);
            }
            else return edgeObject;
        });

        var nodesNotInEdges = node.filter(function (nodeObject) {
            return nodesInEdges.indexOf(nodeObject[property]) < 0;
        });

        nodesNotInEdges.style("opacity", "0.1");
        edgesNotInArray.style("opacity", "0.1");

    }

    /**
     * Highlights nodes from array using property as filter and changes the opacity of the rest of nodes
     * @param {array} nodeArray
     * @param {string} property of the edge to filter
     */
    function highlightNodes(nodeArray, property) {
        // Filter not mapped nodes to change opacity
        var nodesNotInArray = svg.selectAll(".node").filter(function (el) {
            return nodeArray.indexOf(el[property]) < 0;
        });

        // Not mapped links
        var notMappedEdges = g.selectAll(".link").filter(function (el) {
            // Source and target should be present in the edge
            return !(nodeArray.indexOf(el.source[property]) >= 0 || nodeArray.indexOf(el.target[property]) >= 0);
        });

        nodesNotInArray.style("opacity", "0.1");
        notMappedEdges.style("opacity", "0.1");
    }


    // Call freezeGraph when a key is pressed, freezeGraph checks whether this key is "Space" that triggers the freeze
    d3.select(window).on("keydown", freezeGraph);


    /////////////////////////////////////////////////////////////////////////
    // Build the node selection toggle and creates hashmap nodeNames to IDs /
    /////////////////////////////////////////////////////////////////////////

    // Build the node unordered list
    nodePanel.append("<ul id='node-list-ul' class='list-group checked-list-box not-rounded'></ul>");

    // Variable with all node names
    var nodeNames = [];

    // Create node list and create an array with duplicates
    $.each(graph.nodes, function (key, value) {

        nodeNames.push(value.name);

        $("#node-list-ul").append("<li class='list-group-item'><input class='node-checkbox' type='checkbox'>" +
            "<div class='circle'></div><span class='node-" + value.id + "'>" + value.name + "</span></li>");
    });


    // Highlight only selected nodes in the graph
    $("#get-checked-nodes").on("click", function (event) {
        event.preventDefault();
        var checkedItems = [];
        $(".node-checkbox:checked").each(function (idx, li) {
            // Get the class of the span element (node-ID) Strips "node-" and evaluate the string to integer
            checkedItems.push(li.parentElement.childNodes[2].className.replace("node-", ""))
        });

        resetAttributes();
        highlightNodes(checkedItems, 'id');
        resetAttributesDoubleClick();

    });

    ///////////////////////////////////////
    // Build the edge selection toggle
    ///////////////////////////////////////


    // Build the node unordered list
    edgePanel.append("<ul id='edge-list-ul' class='list-group checked-list-box not-rounded'></ul>");


    function zoomed() {
        //Transform svg and update convex hull
        g.attr("transform", d3.event.transform);
    }

    // Zoomming/Panning functionality
    svg.call(d3.zoom()
        .scaleExtent([minZoom, maxZoom])
        .on("zoom", zoomed))
        .on("dblclick.zoom", null);

    /// Convex Hull Specific

    $("#get-checked-edges").on("click", function (event) {
        event.preventDefault();

        var checkedItems = [];
        $(".edge-checkbox:checked").each(function (idx, li) {
            checkedItems.push(li.parentElement.childNodes[1].id);
        });

        resetAttributes();

        highlightEdges(checkedItems, 'id');

        resetAttributesDoubleClick();
    });


    // Update Node Dropdown
    $("#node-search").on("keyup", function () {
        // Get value from search form (fixing spaces and case insensitive
        var searchText = $(this).val();
        searchText = searchText.toLowerCase();
        searchText = searchText.replace(/\s+/g, "");

        $.each($("#node-list-ul")[0].childNodes, updateNodeArray);

        function updateNodeArray() {
            var currentLiText = $(this).find("span")[0].innerHTML,
                showCurrentLi = ((currentLiText.toLowerCase()).replace(/\s+/g, "")).indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        }
    });

    // Update Edge Dropdown
    $("#edge-search").on("keyup", function () {
        // Get value from search form (fixing spaces and case insensitive
        var searchText = $(this).val();
        searchText = searchText.toLowerCase();
        searchText = searchText.replace(/\s+/g, "");

        $.each($("#edge-list-ul")[0].childNodes, updateEdgeArray);

        function updateEdgeArray() {

            var currentLiText = $(this).find("span")[0].innerHTML,
                showCurrentLi = ((currentLiText.toLowerCase()).replace(/\s+/g, "")).indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        }
    });


    var highlightButton = $("#highlight-button");
    highlightButton.off("click"); // It will unbind the previous click if multiple graphs has been rendered

    // Highlight stuffs
    highlightButton.click(function (event) {
        event.preventDefault();

        // Reduce opacity of all nodes/edges to minimum
        svg.selectAll(".node").style("opacity", "0.1");
        svg.selectAll(".link").style("opacity", "0.1");

        $(".highlight-checkbox:checked").each(function (idx, li) {
            var highlightSpan = li.parentElement.parentElement.childNodes[3];

            var spanClass = highlightSpan.className.split("-");

        });

        resetAttributesDoubleClick()

    });


    ///////////////////////
    // Tool modal buttons /
    ///////////////////////

    // Hide node names button

    var hideNodeNames = $("#hide-node-names");

    hideNodeNames.off("click"); // It will unbind the previous click if multiple graphs has been rendered

    // Hide text in graph
    hideNodeNames.on("click", function () {
        svg.selectAll(".node-name").style("display", "none");
    });

    var restoreNodeNames = $("#restore-node-names");

    restoreNodeNames.off("click"); // It will unbind the previous click if multiple graphs has been rendered

    // Hide text in graph
    restoreNodeNames.on("click", function () {
        svg.selectAll(".node-name").style("display", "block");
    });

    var restoreAll = $("#restore");

    restoreAll.off("click"); // It will unbind the previous click if multiple graphs has been rendered

    // Restore all
    restoreAll.on("click", function () {
        resetAttributes();
    });
}

$(document).ready(function () {

    // render network
    initD3Force(network);

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
