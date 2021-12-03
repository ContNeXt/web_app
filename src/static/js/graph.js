// graph.js

// D3 graph (v4)
// set the dimensions and margins of the graph
var margin = {top: 100, right: 30, bottom: 30, left: 1000},
  width = 600 - margin.left - margin.right,
  height = 600 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#graph")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

d3.json("static/js/0000029.json", function(data) {

  // Initialize the links
  var link = svg
    .selectAll("line")
    .data(data.links)
    .enter()
    .append("line")
      .style("stroke", "#aaa")

  // Initialize the nodes
  var node = svg
    .selectAll("circle")
    .data(data.nodes)
    .enter()
    .append("circle")
      .attr("r", 5)
      .style("fill", "#69b3a2")
  // Add name to each node
  node.append("title")
      .text(function(d) { return d.name; });


  // Create a force graph
  // needs 3 forces: link, charge, center
  var simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink()
            .id(function(d) { return d.name; })  // id: Specifies by which attribute the nodes are linked (name)
            .links(data.links)
      )
      .force("charge", d3.forceManyBody().strength(-20))     //  Adds repulsion between nodes.
      .force("center", d3.forceCenter(width / 2, height / 2))    // Attracts nodes to the center of the svg area
      .on("end", ticked);

  // Run at each iteration of the force algorithm, updates the nodes position.
  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
         .attr("cx", function (d) { return d.x+6; })
         .attr("cy", function(d) { return d.y-6; });
  }

});
