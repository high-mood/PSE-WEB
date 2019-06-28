/**
 * Shows a line chart with information of song metric history.
 *
 * This file generates two different line charts displaying a user's song metric history.
 * As such it is structured in two parts:
 * 
 * The line chart for "songs" takes the last *n* songs of a user and displays them to
 * show a user their song metric history over time.
 * 
 * The second way of displaying this data is using the "days" line chart. Here the user
 * selects a number of days, where for each day the average of every metric is calculated
 * and that average is displayed per metric per day
 * 
 * @see {@link https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89} for the code base by Gord Lea
 * @author Stan van den Broek
 * @author Mitchell van den Bulk
 * @author Mo Diallo
 * @author Arthur van Eeden
 * @author Elijah Erven
 * @author Henok Ghebrenigus
 * @author Jonas van der Ham
 * @author Mounir El Kirafi
 * @author Esmeralda Knaap
 * @author Youri Reijne
 * @author Siwa Sardjoemissier
 * @author Barry de Vries
 * @author Jelle Witsen Elias
 */


/**
 * @summary Fills dataset with usable data for d3.
 *
 * @param {Object} dataset
 * @param {Object} data
 * @param {String} chartType
 * @returns
 */
function fillDataset(dataset, data, chartType) {
    var dataKey;
    if (chartType == "songs") {
        dataKey = "metric_over_time";
    }
    else if (chartType == "days") {
        dataKey = "dates";
    }

    for (var metric in dataset) {
        var value = dataset[metric];
        for (var i in d3.range(data[dataKey].length)) {
            value.push({'y': data[dataKey][i][metric]});
        }
    }
    return dataset;
}

/**
 * @summary Gets all scales for linechart.
 *
 * @param {Object} data
 * @param {Object} dataset
 * @param {Number} height
 * @param {Number} width
 * @returns
 */
function getScalesSongs(data, dataset, height, width) {
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

    return [xScale, yScale, yScaleTempo, yScaleMoods, xScaleTicks];
}

// 
/**
 * @summary Create tooltip for song history chart.
 *
 */
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
        .style("border-radius", "10px")
        .style("text-align", "center");
    
    d3.select("#tooltipSongs").append("text").attr("id", "tooltiptextSongs")
        .style("color", "#000000");
}

function getScalesDays(data, dataset, height, width) {
    var parseTime = d3.timeParse("%Y-%m-%d");
    
    // for ordinal date scale
    var dates = [];
    for (val in data["dates"]) {
        dates.push(parseTime(data["dates"][val]["date"]));
    }
    dates = dates.reverse();

    // basic scales
    xScaleTime = d3.scalePoint()
        .domain(dates)
        .range([0, width]);
    yScale = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);
    xScale = d3.scaleLinear()
        .domain([data.dates.length - 1, 0])
        .range([0, width]);
    
    
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
    
    // mood scale
    yScaleMoods = d3.scaleLinear()
        .domain([-10, 10])
        .range([height, 0]);

        return [dates, xScale, yScale, yScaleTempo, yScaleMoods];
}

function createDaysTooltip() {
    // make tooltip
    var tooltip = document.createElement("div");
    
    tooltip.setAttribute("id", "tooltipDays");
    document.getElementById("lineDays").appendChild(tooltip);

    d3.select("#tooltipDays").append("span")
        .attr("id", "tooltipDaysSpan");
    
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
        .style("text-align", "center")
    
    // append text to tooltip
    d3.select("#tooltipDaysSpan").append("text")
        .attr("id", "tooltiptextDays")
        .style("color", "#000000");
}

/**
 *
 *
 * @param {*} svg
 * @param {*} xScaleTicks
 * @param {*} yScale
 * @param {*} yScaleTempo
 * @param {*} yScaleMoods
 * @param {*} height
 * @param {*} width
 * @returns
 */
function createAxes(svg, xScaleTicks, yScale, yScaleTempo, yScaleMoods, height, width) {
    // create axes
    svg.append("g")
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
    return svg;
}

// draws line for song history linechart
/**
 * 
 * @param {*} svgId 
 * @param {Object} dataset 
 * @param {*} name 
 * @param {Object} data 
 */
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

// Draws line for days chart in specified svg
function drawLineDays(svgId, dataset, name) {
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
        .style("fill", "none")
        .style("stroke", color)
        .style("stroke-width", 3);


    // circles with mouse over functionality
    svg.selectAll("." + name + "daysdot")
    .data(dataset)
    .enter().append("circle")
    .attr("class", name + "daysdot")
    .attr("cx", function(d, i) { return xScale(i) })
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
    .attr("r", 3)
    .style("fill", color)
    .on("mouseover", function(y, x) { 
        var value = Math.round(dataset[x]['y'] * 100) / 100;
        d3.select("#tooltipDays")
            .transition()
                .duration(200)
                .style("opacity", 1)
                .style("top", (event.clientY - 40) + "px")
                .style("left", event.clientX + "px")
                .style("background-color", color)
                .style("width", "160px")
                .style("height", "30px");

        d3.select("#tooltiptextDays")
            .html(name + ": " + value);
        })
    .on("mouseout", function() {
        d3.select("#tooltipDays")
            .transition()
                .duration(200)
                .style("opacity", 0)
                .style("width", 0)
                .style("height", 0);
        d3.select("#tooltiptextDays")
            .html("");
        })
}



/**
 * @summary Trims song name for tooltip.
 *
 * @param {*} name
 * @returns
 */
function trimSongName(name) {
    /**
     * Switches analytics chart description based on currently show chart.
     *
     * @param {String}   chartName           Name of the chart to display a description for.
     */
    if (name.length > 20) {
        return name.slice(0, 17).concat("...");
    }
    else {
        return name;
    }
}

// drops datapoints with no information from data
/**
 *
 *
 * @param {Object} data
 * @returns
 */
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

/**
 *
 *
 * @param {Object} data
 * @param {*} id
 * @param {*} retriggered
 */
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
    dataset = fillDataset(dataset, data, "songs");

    // dimensions and margins of graph
    var margin = {top: 20, right: 80, bottom: 30, left: 30};
    var width = 600 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    [xScale, yScale, yScaleTempo, yScaleMoods, xScaleTicks] = getScalesSongs(data, dataset, height, width);

    // make svg and g html element
    var svgId = "songsSvg";
    var svg = d3.select("#" + id).append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", "-20 -20 600 320")
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .attr("id", svgId);
    
    svg = createAxes(svg, xScaleTicks, yScale, yScaleTempo, yScaleMoods, height, width);
    createSongsTooltip();
    
    drawLines("songs", svgId, dataset, retriggered, data);
}

function createLineGraphDays(data, id, retriggered) {
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
    
    // fill dataset with usable d3 data
    dataset = fillDataset(dataset, data, "days")

    // dimensions and margins of graph
    var margin = {top: 20, right: 80, bottom: 30, left: 30};
    var width = 600 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    [dates, xScale, yScale, yScaleTempo, yScaleMoods] = getScalesDays(data, dataset, height, width);

    // make svg and g html element
    var svgId = "daysSvg";
    var svg = d3.select("#" + id).append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", "-20 -20 600 320")
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .attr("id", svgId);


    svg = createAxes(svg, xScale, yScale, yScaleTempo, yScaleMoods, height, width);

    createDaysTooltip();

    // draw proper lines
    drawLines('days', svgId, dataset, retriggered, null);
}

// 
/**
 * @summary Draws all lines in chart.
 *
 * @param {*} charttype
 * @param {*} svgId
 * @param {Object} dataset
 * @param {*} retriggered
 * @param {Object} data
 */
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

/**
 * @summary Trims song name for tooltip.
 *
 * @param {*} name
 * @returns
 */
function trimSongName(name) {
    /**
     * Switches analytics chart description based on currently show chart.
     *
     * @param {String}   chartName           Name of the chart to display a description for.
     */
    if (name.length > 20) {
        return name.slice(0, 17).concat("...");
    }
    else {
        return name;
    }
}

// 
/**
 * @summary Drops datapoints with no information from data.
 *
 * @param {Object} data
 * @returns
 */
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