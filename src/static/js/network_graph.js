// network_graph.js
// D3 force graph (v5)
// TODO image too big to load, fix

  // Initialize svg in <div> element
  var svg = d3.select("#graph").select("svg");
  var width = svg.attr("width");
  var height = svg.attr("height");

  // Get data from JSON file
  d3.json("0000029.json", function(graph) {

    // Inside this block, the data has been loaded

    // Create a force graph
    // needs 3 forces: link, charge, center
    var simulation = d3
        .forceSimulation(graph.nodes)
        .force(
            "link",
            // id specifies by which attribute the nodes are linked (name)
            d3.forceLink(graph.links.id(function(d) {
                    return d.name;
                })
            .links(graph.links)
        )
        .force("charge", d3.forceManyBody().strength(-20))
        .force("center", d3.forceCenter(width / 2, height / 2)));

    // Create <line> SVG element for each link
    var link = svg
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter()
        .append("line")
        .attr("stroke-width", function(d){
          return 3;
        });

    // Create <circle> SVG element for each node
    var node = svg
        .append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(graph.nodes)
        .enter()
        .append("circle")
        .attr("r",5)
        .attr("fill", "orange")
        .attr("stroke", "yellow");

    // Add name to each node
    node.append("title")
        .text(function(d) { return d.name; });

    // We bind the positions of the SVG elements
    // to the positions of the dynamic force-directed
    // graph, at each time step.
    force.on("tick", function() {
      link.attr("x1", function(d){return d.source.x})
          .attr("y1", function(d){return d.source.y})
          .attr("x2", function(d){return d.target.x})
          .attr("y2", function(d){return d.target.y});

      node.attr("cx", function(d){return d.x})
          .attr("cy", function(d){return d.y});
    });

  });
