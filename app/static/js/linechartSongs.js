// Code basis by Gord Lea: https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89
// Legend code from https://www.d3-graph-gallery.com/graph/custom_legend.html

var xScale, yScale, yScaleTempo;

function createLineGraphSongs(data, id) {

//    console.log(data);

    // dataset, unused metrics are commented out
    var dataset = {
        // "energy": [],
        // "positivity": [],
        "acousticness": [],
        "danceability": [],
        // "duration_ms": [],
        "energy": [],
        "instrumentalness": [],
        // "key": [],
        "liveness": [],
        // "loudness": [],
        // "mode": [],
        "speechiness": [],
        "tempo": [],
        "valence": [],
    }

    // fill dataset with usable d3 data
    for (var key in dataset) {
        var value = dataset[key]
        for (var i in d3.range(data.metric_over_time.length)) {
            value.push({'y': data.metric_over_time[i][key]})
        }
    }

    // dimensions and margins of graph
    var margin = {top: 20, right: 80, bottom: 30, left: 30};
    var width = 600 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    // scales
    xScale = d3.scaleLinear()
        .domain([data.metric_over_time.length - 1, 0])
        .range([0, width])
    yScale = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);

    // array to calculate max and min tempo for scale
    tempoArray = []
    for (var i in dataset["tempo"]) {
        tempoArray.push(dataset["tempo"][i].y)
    }
    tempoFloor = Math.floor(d3.min(tempoArray) / 10) * 10

    // tempo scale
    yScaleTempo = d3.scaleLinear()
        .domain([tempoFloor, d3.max(tempoArray)])
        .range([height, 0]); // output

    // make svg and g html element
    var svgId = "lineSvg"
    var svg = d3.select("#" + id).append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", "-20 -20 600 400")
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .attr("id", svgId);

    // simple scale to show on x axis
    var xScaleTicks = d3.scaleOrdinal()
        .domain(["past", "now"])
        .range([0, width])

    // create axes
    xAxis = svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height / 2 + ")")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScaleTicks)
        .ticks(10))
    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale));
        


    // call tempo y axis
    svg.append("g")
        .attr("class", "y axis tempo")
        .attr("transform", "translate(" + width + ", 0)")
        .call(d3.axisRight(yScaleTempo).ticks(10))
        .append("text")
        .attr("transform",
              "rotate(90) translate(" + height / 2 + ", -40)")
        .style("text-anchor", "middle")
        .text("tempo (BPM)")
    
    // make tooltip
    var tooltip = document.createElement("div")
    tooltip.setAttribute("id", "tooltip")
    document.getElementById("body").appendChild(tooltip)
    
    // set proper style for tooltip
    d3.select("#tooltip")
        .style("width", "160px")
        .style("height", "30px")
        .style("position", "fixed")
        .style("background-color", "steelblue")
        .style("top", "0px")
        .style("left", "0px")
        .style("opacity", 0)
        .style("border-radius", "10px")
    
    d3.select("#tooltip").append("text").attr("id", "tooltiptext")
        .style("color", "#000000")
    
    // draw all lines
    for (var key in dataset) {
        drawLine(svgId, dataset[key], key);
    }

    // show only startLines at page load
    var startLines = ["danceability", "energy", "liveness"]
    startStates(startLines)
}


function drawLine(svgId, dataset, name) {

    // make correct d3 line generator
    var line;
    if (name == "tempo") {
        line = d3.line()
            .x(function(d, i) { return xScale(i); })
            .y(function(d) { return yScaleTempo(d.y); })
            .curve(d3.curveMonotoneX)
    }
    else {
        line = d3.line()
            .x(function(d, i) { return xScale(i); })
            .y(function(d) { return yScale(d.y); })
            .curve(d3.curveMonotoneX)
    }

    // give line color of corresponding button
    var svg = d3.select("#" + svgId);
    var color = d3.select("#" + name).style("background-color")

    // draw lines
    svg.append("path")
        .data([dataset])
        .attr("class", "line")
        .attr("id", name + "line")
        .attr("d", line)
        .style("fill", "none")
        .style("stroke", color)
        .style("stroke-width", 3)


    // circles with mouse over functionality
    svg.selectAll("." + name + "dot")
    .data(dataset)
    .enter().append("circle")
    .attr("class", name + "dot")
    .attr("cx", function(d, i) { return xScale(i) })
    .attr("cy", function(d) {   if (name == "tempo") {
                                    return yScaleTempo(d.y)
                                } 
                                else {
                                    return yScale(d.y)
                                }
                            })
    .attr("r", 4)
    .style("fill", color)
    .on("mouseover", function(y, x) { 
        var value = Math.round(dataset[x]['y'] * 100) / 100;
        d3.select("#tooltip")
            .transition()
                .duration(200)
                .style("opacity", 1)
                .style("top", (event.clientY - 30) + "px")
                .style("left", event.clientX + "px")
                .style("background-color", color)

        d3.select("#tooltiptext")
            .html(name + ": " + value)
        })
    .on("mouseout", function() {
        d3.select("#tooltip")
            .transition()
                .duration(200)
                .style("opacity", 0)
        })
}

// hides a given line
function hideLine(name) {
    d3.select("#" + name + "line")
        .style("visibility", "hidden")
    d3.selectAll("." + name + "dot")
        .style("visibility", "hidden") 

    if (name == "tempo") {
        d3.select(".tempo.axis")
            .style("visibility", "hidden")
    }
}

// shows a given line
function showLine(name) {
    d3.select("#" + name + "line")
        .style("visibility", "visible")
    d3.selectAll("." + name + "dot")
        .style("visibility", "visible")

    if (name == "tempo") {
        d3.select(".tempo.axis")
            .style("visibility", "visible")
    }
}