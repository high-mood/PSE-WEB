/*
 * Shows a line chart with information of song history of specific user.
 * Code basis by Gord Lea: 
 * https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89
 */

var xScale, yScale, yScaleTempo, yScaleMoods, data;

// fills dataset
function fillDataset(dataset, data) {
    for (var key in dataset) {
        var value = dataset[key];
        for (var i in d3.range(data.metric_over_time.length)) {
            value.push({'y': data.metric_over_time[i][key]});
        }
    }
    return dataset;
}

// gets all scales for linechart
function getScales(data, dataset, height, width) {
    // scales
    xScale = d3.scaleLinear()
        .domain([data.metric_over_time.length - 1, 0])
        .range([0, width]);
    yScale = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);

    // array to calculate max and min tempo for scale
    tempoArray = [];
    for (var i in dataset["tempo"]) {
        tempoArray.push(dataset["tempo"][i].y);
    }
    tempoFloor = Math.floor(d3.min(tempoArray) / 10) * 10;

    // tempo scale
    yScaleTempo = d3.scaleLinear()
        .domain([tempoFloor, d3.max(tempoArray)])
        .range([height, 0]);


    // tempo scale
    yScaleMoods = d3.scaleLinear()
        .domain([-10, 10])
        .range([height, 0]);

    // simple scale to show on x axis
    var xScaleTicks = d3.scaleOrdinal()
        .domain(["past", "now"])
        .range([0, width]);

    return [dataset, xScale, yScale, yScaleTempo, yScaleMoods, xScaleTicks];
}

// create tooltip for song history chart
function createSongsTooltip() {
    // make tooltip
    var tooltip = document.createElement("div");
    tooltip.setAttribute("id", "tooltipSongs");
    $('#lineSongs').append(tooltip);
    
    // set proper style for tooltip
    d3.select("#tooltipSongs")
        .style("width", "160px")
        .style("height", "40px")
        .style("position", "fixed")
        .style("background-color", "steelblue")
        .style("top", "0px")
        .style("left", "0px")
        .style("opacity", 0)
        .style("border-radius", "10px");
    
    d3.select("#tooltipSongs").append("text").attr("id", "tooltiptextSongs")
        .style("color", "#000000");
}

function createAxes(svg, xScaleTicks, yScale, yScaleTempo, yScaleMoods, height, width) {
    // create axes
    xAxis = svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height / 2 + ")")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScaleTicks)
        .ticks(10));
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
        .text("tempo (BPM)");


    // call moods y axis
    svg.append("g")
        .attr("class", "y axis moods")
        .attr("transform", "translate(" + width + ", 0)")
        .call(d3.axisRight(yScaleMoods).ticks(10))
        .append("text")
            .attr("transform",
                  "rotate(90) translate(" + height / 2 + ", -40)")
            .style("text-anchor", "middle")
            .text("Moods");
    return [svg, xAxis];
}

function createLineGraphSongs(data, id, retriggered) {

    // clear div before proceeding
    $(`#${id}`).empty();

    // dataset for d3
    var dataset = {
        "excitedness": [],
        "happiness": [],
        "acousticness": [],
        "danceability": [],
        "energy": [],
        "instrumentalness": [],
        "liveness": [],
        "speechiness": [],
        "tempo": [],
        "valence": [],
    };

    data = dropNullData(data);

    // fill dataset with usable d3 data
    dataset = fillDataset(dataset, data);

    // dimensions and margins of graph
    var margin = {top: 20, right: 80, bottom: 30, left: 30};
    var width = 600 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    [dataset, xScale, yScale, yScaleTempo, yScaleMoods, xScaleTicks] = getScales(data, dataset, height, width);

    // make svg and g html element
    var svgId = "songsSvg";
    var svg = d3.select("#" + id).append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", "-20 -20 600 320")
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .attr("id", svgId);
    
    svg, xAxis = createAxes(svg, xScaleTicks, yScale, yScaleTempo, yScaleMoods, height, width);
    createSongsTooltip();
    
    drawLines("songs", svgId, dataset, retriggered, data);
}

// draws all lines in chart
function drawLines(charttype, svgId, dataset, retriggered, data) {
    // draw all lines, show wanted ones
    for (var key in dataset) {
        if (!retriggered && charttype != "days") {
            if (charttype == "songs") {
                drawLineSongs(svgId, dataset[key], key, data);
            }
            else {
                drawLineDays(svgId, dataset[key], key);
            }
            showLine(key);
            if (key != "happiness" && key != "excitedness") {      
                $("#" + key).trigger("click");
            }
        }
        else {
            if (charttype == "songs") {
                drawLineSongs(svgId, dataset[key], key, data);
            }
            else {
                drawLineDays(svgId, dataset[key], key);
            }
            if ($(`#${key}`).css("opacity") == "1") {
                showLine(key);
            }
            else {
                hideLine(key);
            }
        } 
    }
}

// draws line for song history linechart
function drawLineSongs(svgId, dataset, name, data) {

    // make correct d3 line generator
    var line;
    if (name == "tempo") {
        line = d3.line()
            .x(function(d, i) { return xScale(i); })
            .y(function(d) { return yScaleTempo(d.y); })
            .curve(d3.curveMonotoneX);
    }
    else if (name == "happiness" || name == "excitedness") {
        line = d3.line()
            .x(function(d, i) { return xScale(i); })
            .y(function(d) { return yScaleMoods(d.y); })
            .curve(d3.curveMonotoneX);
    }
    else {
        line = d3.line()
            .x(function(d, i) { return xScale(i); })
            .y(function(d) { return yScale(d.y); })
            .curve(d3.curveMonotoneX);
    }

    // give line color of corresponding button
    var svg = d3.select("#" + svgId);
    var color = d3.select("#" + name).style("background-color");

    // draw lines
    svg.append("path")
        .data([dataset])
        .attr("class", "line")
        .attr("id", name + "line")
        .attr("d", line)
        .style("visibility", "hidden")
        .style("fill", "none")
        .style("stroke", color)
        .style("stroke-width", 3);


    // circles with mouse over functionality
    svg.selectAll("." + name + "songdot")
    .data(dataset)
    .enter().append("circle")
    .attr("class", name + "songdot")
    .attr("cx", function(d, i) { return xScale(i); })
    .attr("cy", function(d) {   if (name == "tempo") {
                                    return yScaleTempo(d.y);
                                }
                                else if (name == "happiness" || 
                                         name == "excitedness") {
                                    return yScaleMoods(d.y);
                                }
                                else {
                                    return yScale(d.y);
                                }
                            })
    .attr("r", 4)
    .style("fill", color)
    .on("mouseover", function(y, x) { 
        var value = Math.round(dataset[x]['y'] * 100) / 100;
        d3.select("#tooltipSongs")
            .transition()
                .duration(200)
                .style("opacity", 1)
                .style("top", (event.clientY - 40) + "px")
                .style("left", event.clientX + "px")
                .style("background-color", color)
                .style("width", "160px")
                .style("height", "40px");

        d3.select("#tooltiptextSongs")
            .html(name + ": " + value + "<br>" + 
                  trimSongName(data["metric_over_time"][x]["name"]));
        })
    .on("mouseout", function() {
        d3.select("#tooltipSongs")
            .transition()
                .duration(200)
                .style("opacity", 0)
                .style("width", "0")
                .style("height", "0");

        d3.select("#tooltiptextSongs")
            .html("");
    })
}

// trims song name for tooltip
function trimSongName(name) {
    if (name.length > 20) {
        return name.slice(0, 17).concat("...");
    }
    else {
        return name;
    }
}

// drops datapoints with no information from data
function dropNullData(data) {
    for (var i in data["metric_over_time"]) {
        for (var key in data["metric_over_time"][i]) {
            if (data["metric_over_time"][i][key] == null) {
                data["metric_over_time"].splice(i, 1);
                break;
            }
        }
    }
    return data;
}