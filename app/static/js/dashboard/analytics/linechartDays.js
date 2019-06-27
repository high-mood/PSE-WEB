// Code basis by Gord Lea: https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89
// Legend code from https://www.d3-graph-gallery.com/graph/custom_legend.html

var xScale, yScale, yScaleTempo, yScaleMoods;

var lineNames = ["excitedness", "happiness", "acousticness", "danceability", 
                 "energy", "instrumentalness", "liveness", "speechiness", 
                 "tempo", "valence"];

function createLineGraphDays(data, id) {
    // dataset, unused metrics are commented out
    var dataset = {
        "excitedness": [],
        "happiness": [],
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
        for (var i in d3.range(data.dates.length)) {
            value.push({'y': data.dates[i][key]})
        }
    }

    // dimensions and margins of graph
    var margin = {top: 20, right: 80, bottom: 30, left: 30};
    var width = 600 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    // for (i = 0; i < 8; i++) {
    //     data.dates[i]["date"] = "2019-06-" + data.dates[i]["date"]
    // }
    var minDate = data.dates[data.dates.length - 1].date
    var maxDate = data.dates[0].date
    // debugger;

    var parseTime = d3.timeParse("%Y-%m-%d")
    // var parseTime = d3.timeParse("%d")
    
    // var parsedMinDate = parseTime("2019-06-21")
    var parsedMinDate = parseTime(minDate)
    var parsedMaxDate = parseTime(maxDate)

    var dates = [];
    for (val in data.dates) {
        dates.push(parseTime(data.dates[val]["date"]));
    }
    dates = dates.reverse()
    // scales
    // xScaleTime = d3.scaleTime()
    //     .domain(d3.extent(dates))
    //     .range([0, width])
    xScaleTime = d3.scalePoint()
        .domain(dates)
        .range([0, width])
    yScale = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);
        
       
    xScale = d3.scaleLinear()
        .domain([data.dates.length - 1, 0])
        .range([0, width])
    
    
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
    
        // tempo scale
    yScaleMoods = d3.scaleLinear()
        .domain([-10, 10])
        .range([height, 0]); // output

    // make svg and g html element
    var svgId = "daysSvg"
    var svg = d3.select("#" + id).append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", "-20 -20 600 320")
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .attr("id", svgId);


    // create axes
    xAxis = svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height / 2 + ")")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScaleTime)
            .tickValues(dates)
            .tickFormat(d3.timeFormat("%Y-%m-%d")))
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

    // call moods y axis
    svg.append("g")
        .attr("class", "y axis moods")
        .attr("transform", "translate(" + width + ", 0)")
        .call(d3.axisRight(yScaleMoods).ticks(10))
        .append("text")
            .attr("transform",
                  "rotate(90) translate(" + height / 2 + ", -40)")
            .style("text-anchor", "middle")
            .text("Moods")
    
    // make tooltip
    var tooltip = document.createElement("div")
    tooltip.setAttribute("id", "tooltipDays")
    document.getElementById("lineDays").appendChild(tooltip)
    
    // set proper style for tooltip
    d3.select("#tooltipDays")
        .style("width", "160px")
        .style("height", "30px")
        .style("position", "fixed")
        .style("background-color", "steelblue")
        .style("top", "0px")
        .style("left", "0px")
        .style("opacity", 0)
        .style("border-radius", "10px")
    
    d3.select("#tooltipDays").append("text").attr("id", "tooltiptextDays")
        .style("color", "#000000")
    
    // draw all lines, show wanted ones
    for (var key in dataset) {
        drawLineDays(svgId, dataset[key], key);
        showLine(key);

        // only show happiness and excitedness on page load
        if (key != "happiness" && key != "excitedness") {
            $("#" + key).trigger("click")
        }
    }
}


function drawLineDays(svgId, dataset, name) {
    // make correct d3 line generator
    var line;
    if (name == "tempo") {
        line = d3.line()
            .x(function(d, i) { return xScale(i); })
            .y(function(d) { return yScaleTempo(d.y); })
            .curve(d3.curveMonotoneX)
    }
    else if (name == "happiness" || name == "excitedness") {
        line = d3.line()
            .x(function(d, i) { return xScale(i); })
            .y(function(d) { return yScaleMoods(d.y); })
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
    svg.selectAll("." + name + "daysdot")
    .data(dataset)
    .enter().append("circle")
    .attr("class", name + "daysdot")
    .attr("cx", function(d, i) { return xScale(i) })
    .attr("cy", function(d) {   if (name == "tempo") {
                                    return yScaleTempo(d.y)
                                } 
                                else if (name == "happiness" || 
                                         name == "excitedness") {
                                    return yScaleMoods(d.y)
                                }
                                else {
                                    return yScale(d.y)
                                }
                            })
    .attr("r", 3)
    .style("fill", color)
    .on("mouseover", function(y, x) { 
        var value = Math.round(dataset[x]['y'] * 100) / 100;
        d3.select("#tooltipDays")
            .transition()
                .duration(200)
                .style("opacity", 1)
                .style("top", (event.clientY - 30) + "px")
                .style("left", event.clientX + "px")
                .style("background-color", color)
                .style("width", "160px")
                .style("height", "30px")

        d3.select("#tooltiptextDays")
            .html(name + ": " + value)
        })
    .on("mouseout", function() {
        d3.select("#tooltipDays")
            .transition()
                .duration(200)
                .style("opacity", 0)
                .style("width", "0")
                .style("height", "0")
        })
}

function toggleLine(buttonId) {
    // var name = d3.select("#" + buttonId).text();
    button = $(`#${buttonId}`)
    if (button.css('opacity') == '1') {
        button.css('opacity', '0.3');
    }
    else {
        button.css('opacity', '1');
    }
    var color = d3.select("#" + buttonId).style("backgroundColor")
    var toggled = d3.select("#" + buttonId + "line").style("visibility")

    if (toggled == "hidden") {
        showLine(buttonId)
    }
    else {
        hideLine(buttonId)
    }
}

function toggleAll() {
    // check if all buttons toggled
    var allToggled = true;
    for (var i in lineNames) {
        if (d3.select("#" + lineNames[i] + "line").style("visibility") == "hidden") {
            allToggled = false;
            break;
        }
    }
    if (allToggled) {
        for (var i in lineNames) {
            toggleLine(lineNames[i])
        }
    }
    else {
        for (var i in lineNames) {
            if (d3.select("#" + lineNames[i] + "line").style("visibility") == "hidden") {
                toggleLine(lineNames[i])
            }
        }
    }
}



// hides a given line, shows and hides relevant axes
function hideLine(name) {

    d3.selectAll("#" + name + "line")
        .style("visibility", "hidden")
    d3.selectAll("." + name + "daysdot")
        .style("visibility", "hidden") 
    d3.selectAll("." + name + "songdot")
        .style("visibility", "hidden") 

    if (name == "tempo") {
        d3.selectAll(".tempo.axis")
            .style("visibility", "hidden")


        if (d3.select("#excitednessline").style("visibility") == "visible" ||
            d3.select("#happinessline").style("visibility") == "visible") {
            d3.selectAll(".moods.axis").style("visibility", "visible");
        }
    }

    else if (name == "happiness") {
        if (d3.select("#excitednessline").style("visibility") == "hidden") {
            d3.selectAll(".moods.axis").style("visibility", "hidden")
            if (d3.select("#tempoline").style("visibility") == "visible") {
                d3.selectAll(".tempo.axis").style("visibility", "visible")
            }           
        }
    }
    else if (name == "excitedness") {
        if (d3.select("#happinessline").style("visibility") == "hidden") {
            d3.selectAll(".moods.axis").style("visibility", "hidden")
            if (d3.select("#tempoline").style("visibility") == "visible") {
                d3.selectAll(".tempo.axis").style("visibility", "visible")
            }           
        }
    }
}

// shows a given line
function showLine(name) {
    d3.selectAll("#" + name + "line")
        .style("visibility", "visible")
    d3.selectAll("." + name + "daysdot")
        .style("visibility", "visible")
    d3.selectAll("." + name + "songdot")
        .style("visibility", "visible")

    if (name == "tempo") {
        d3.selectAll(".tempo.axis")
            .style("visibility", "visible")
        d3.selectAll(".moods.axis")
            .style("visibility", "hidden")
    }
    if (name == "happiness" || name == "excitedness") {
        d3.select(".moods.axis")
            .style("visibility", "visible")
        d3.select(".tempo.axis")
            .style("visibility", "hidden")
    }
}