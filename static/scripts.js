
var width;
var height;
var projection, svg, path, g;


function compute_size() {
    var margin = 50;
    width = parseInt(d3.select("#map").style("width"));
    height = window.innerHeight - 2*margin;
}

function init(width, height) {

    // pretty boring projection
    projection = d3.geo.albers()
        .rotate([0, 0]);

    path = d3.geo.path()
        .projection(projection);

    // create the svg element for drawing onto
    svg = d3.select("#map").append("svg")
        .attr("width", width)
        .attr("height", height);

    // graphics go here
    g = svg.append("g");

    // add a white rectangle as background to enable us to deselect a map selection
    g.append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", width)
        .attr("height", height)
        .style("fill", "#fff")
        .on('click', deselect);
}

function deselect() {
    d3.selectAll(".selected").attr("class", "area");
}

function select(d) {
    var id = "#" + d;
    d3.selectAll(".selected").attr("class", "area");
    d3.select(id).attr("class", "selected area")
}


var ids = [];

function draw(boundaries) {

    projection.scale(1).translate([0,0]);

    var b = path.bounds(boundaries);
    var s = .95 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height);
    var t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

    projection.scale(s).translate(t);

    for (var i in boundaries.features) {
        ids.push(boundaries.features[i].properties.id);
    }


    g.selectAll(".area")
        .data(boundaries.features)
        .enter().append("path")
        .attr("class", "area")
        .attr("id", function(d) {return d.properties.id})
        .attr("d", path)
        .on("click", function(d){ return select(d.properties.id)});
}

function load_data(filename) {
    d3.json(filename, function(error, b) {
        if (error) return console.error(error);
        draw(b);
    });
}

compute_size();
init(width, height);
load_data('/static/london.json');


function myLoop () {

    setTimeout(function() {

console.log(ids);
        deselect();
        var id = ids[Math.floor(Math.random()*ids.length)];
        console.log(id);
        select(id);
        myLoop();
    }, 1000);

}

myLoop();