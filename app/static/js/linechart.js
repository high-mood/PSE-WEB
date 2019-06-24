// Code by Gord Lea: https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89

// Legend code from https://www.d3-graph-gallery.com/graph/custom_legend.html
var xScale, yScale;

function createLineGraph(data, id) {

//    console.log(data);



    // var datasetExcite = []
    // var datasetHappy = []
    // var meanExcite = []
    // var meanHappy = []

    var dataset = {
        "acousticness": [],
        "danceability": [],
        // "duration_ms": [],
        "energy": [],
        "instrumentalness": [],
        // "key": [],
        "liveness": [],
        "loudness": [],
        // "mode": [],
        "speechiness": [],
        "tempo": [],
        "valence": [],
    }

    // number of data points
    
    // for (var i in d3.range(n)) {
        //     dataset.push('y': data.songs[i].excitedness)
        //     // datasetHappy.push({'y': data.songs[i].happiness})
        //     // meanExcite.push({'y': data['mean_excitedness']})
        //     // meanHappy.push({'y': data['mean_happiness']})
        // }

    for (var key in dataset) {
        var value = dataset[key]

        for (var i in d3.range(data.metric_over_time.length)) {
            value.push({'y': data.metric_over_time[i][key]})
        }
    }

    // console.log(dataset)

    // Object.keys(dataset).forEach(function(key) {
    //     console.log(key);
    // });

    // console.log(meanExcite)

    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 30, bottom: 30, left: 30};
    var width = 600 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    // 5. X scale will use the index of our data
    xScale = d3.scaleLinear()
        .domain([data.metric_over_time.length - 1, 0]) // input
        .range([0, width])


    // 6. Y scale will use the randomly generate number
    yScale = d3.scaleLinear()
        .domain([0, 1]) // input
        .range([height, 0]); // output


    var svgId = "lineSvg"
    var svg = d3.select("#" + id).append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", "-20 -20 600 400")
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .attr("id", svgId);

    // 3. Call the x axis in a group tag
    xAxis = svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height / 2 + ")")
        .attr("transform", "translate(0," + height + ")")
        // .call(d3.axisBottom(xScale).tickFormat(d3.format("d")))
        .call(d3.axisBottom(xScale)
        .ticks(10))

    // 4. Call the y axis in a group tag
    svg.append("g")
        .attr("class", "y axis")
        // .attr("transform", "translate(" + width / 2 + ", 0)")
        .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

    var lineExcite = d3.line()
    .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
    .y(function(d) { return yScale(d.y); }) // set the y values for the line generator
    .curve(d3.curveMonotoneX) // apply smoothing to the line

    var lineHappy = d3.line()
    .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
    .y(function(d) { return yScale(d.y); }) // set the y values for the line generator
    .curve(d3.curveMonotoneX) // apply smoothing to the line

    // svg.append("path")
    //     .data([datasetExcite])
    //     .attr("class", "line")
    //     .attr("id", "exciteLine")
    //     .attr("d", lineExcite);

    // svg.append("path")
    //     .data([datasetHappy])
    //     .attr("class", "line")
    //     .attr("id", "happyLine")
    //     .attr("d", lineHappy);

    // svg.append("path")
    //     .data([meanExcite])
    //     .attr("class", "line")
    //     .attr("id", "exciteMean")
    //     .attr("d", lineExcite);

    // svg.append("path")
    //     .data([meanHappy])
    //     .attr("class", "line")
    //     .attr("id", "happyMean")
    //     .attr("d", lineHappy);


    
    
    
    
    // Handmade legend
    // var legendY = 150
    // svg.append("circle").attr("cx",width+30).attr("cy",legendY).attr("r", 6).attr("id", "exciteLegend")
    // svg.append("circle").attr("cx",width+30).attr("cy",legendY + 30).attr("r", 6).attr("id", "happyLegend")
    // svg.append("text").attr("x", width+50).attr("y", legendY).text("Excitedness").style("font-size", "15px").attr("alignment-baseline","middle")
    // svg.append("text").attr("x", width+50).attr("y", legendY + 30).text("Happiness").style("font-size", "15px").attr("alignment-baseline","middle")
    // svg.append("circle").attr("cx",width+30).attr("cy",legendY + 60).attr("r", 6).attr("id", "exciteLegendMean")
    // svg.append("circle").attr("cx",width+30).attr("cy",legendY + 90).attr("r", 6).attr("id", "happyLegendMean")
    // svg.append("text").attr("x", width+50).attr("y", legendY + 60).text("Mean excitedness").style("font-size", "15px").attr("alignment-baseline","middle")
    // svg.append("text").attr("x", width+50).attr("y", legendY + 90).text("Mean happiness").style("font-size", "15px").attr("alignment-baseline","middle")
    
    
    
    
    
    var tooltip = document.createElement("div")
    
    tooltip.setAttribute("id", "tooltip")
    
    document.getElementById("body").appendChild(tooltip)
    
    
    d3.select("#tooltip")
    // .attr("class", "tooltip")
    .style("width", "140px")
    .style("height", "30px")
    .style("position", "fixed")
    .style("background-color", "steelblue")
    .style("top", "0px")
    .style("left", "0px")
    .style("opacity", 0)
    .style("border-radius", "10px")
    
    d3.select("#tooltip").append("text").attr("id", "tooltiptext")
        .style("color", "#000000")
    
    for (var key in dataset) {
        drawLine(svgId, dataset[key], key);
        // hideLine(key)
    }



    // 12. Appends a circle for each datapoint 
    // svg.selectAll(".excitedot")
    // .data(datasetExcite)
    // .enter().append("circle") // Uses the enter().append() method
    // .attr("class", "excitedot") // Assign a class for styling
    // .attr("cx", function(d, i) { return xScale(i) })
    // .attr("cy", function(d) { return yScale(d.y) })
    // .attr("r", 5)
    // .on("mouseover", function(y, x) { 
    //     // debugger;
    //     var excitedness = Math.round(datasetExcite[x]['y'] * 100) / 100;
    //     // console.log(happiness);
    //     d3.select("#tooltip")
    //         .transition()
    //             .duration(200)
    //             .style("opacity", 1)
    //             .style("top", (event.clientY - 30) + "px")
    //             .style("left", event.clientX + "px")
    //             .style("background-color", "#ffab00")

    //     d3.select("#tooltiptext")
    //         .html("  excitedness: " + excitedness + "  ")
    //     })
    // .on("mouseout", function() {
    //     d3.select("#tooltip")
    //         .transition()
    //             .duration(200)
    //             .style("opacity", 0)
    //     })


    // svg.selectAll(".happydot")
    // .data(datasetHappy)
    // .enter().append("circle") // Uses the enter().append() method
    // .attr("class", "happydot") // Assign a class for styling
    // .attr("cx", function(d, i) { return xScale(i) })
    // .attr("cy", function(d) { return yScale(d.y) })
    // .attr("r", 5)
    // .on("mouseover", function(y, x) { 
    //     console.log(x)
    //     // debugger;
    //     var happiness = Math.round(datasetHappy[x]['y'] * 100) / 100;
    //     // console.log(happiness);
    //     d3.select("#tooltip")
    //         .transition()
    //             .duration(200)
    //             .style("opacity", 1)
    //             .style("top", (event.clientY - 30) + "px")
    //             .style("left", event.clientX + "px")
    //             .style("background-color", "steelblue")

    //     d3.select("#tooltiptext")
    //         .html("  happiness: " + happiness + "  ")
    //     })
    // .on("mouseout", function() {
    //     d3.select("#tooltip")
    //         .transition()
    //             .duration(200)
    //             .style("opacity", 0)
    //     })

        
    // xAxis.selectAll(".tick")
    // .each(function (d) {
    //     if ( d === 0 ) {
    //         this.remove();
    //     }
    // });
}


function drawLine(svgId, dataset, name) {

    // console.log("Test")

    var line = d3.line()
        .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
        .y(function(d) { return yScale(d.y); }) // set the y values for the line generator
        .curve(d3.curveMonotoneX) // apply smoothing to the line


    var svg = d3.select("#" + svgId);

    var color = d3.select("#" + name).style("background-color")

    // console.log("color: ")
    // console.log(color)

    svg.append("path")
        .data([dataset])
        .attr("class", "line")
        .attr("id", name + "line")
        .attr("d", line)
        .style("fill", "none")
        .style("stroke", color)
        .style("stroke-width", 3)


    // 12. Appends a circle for each datapoint 
    svg.selectAll("." + name + "dot")
    .data(dataset)
    .enter().append("circle")
    .attr("class", name + "dot")
    .attr("cx", function(d, i) { return xScale(i) })
    .attr("cy", function(d) { return yScale(d.y) })
    .attr("r", 3)
    .style("fill", color)
    .on("mouseover", function(y, x) { 
        // debugger;
        var value = Math.round(dataset[x]['y'] * 100) / 100;
        // console.log(happiness);
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


function hideLine(name) {
    d3.select("#" + name + "line")
        .style("visibility", "hidden")
    d3.selectAll("." + name + "dot")
        .style("visibility", "hidden") 
}


function showLine(name) {
    d3.select("#" + name + "line")
        .style("visibility", "visible")
    d3.selectAll("." + name + "dot")
        .style("visibility", "visible")
}