// Code by Gord Lea: https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89

// Legend code from https://www.d3-graph-gallery.com/graph/custom_legend.html

function lineGraph(data, id) {

   console.log(data);

    var dataset = d3.range(data.moods.length).map(function(d) { return {"y": d3.randomUniform(1)() } });
//    console.log(dataset);

    var datasetExcite = []
    var datasetHappy = []
    var meanExcite = []
    var meanHappy = []

    // number of data points
    var n = data.moods.length;

    // for (var i in d3.range(20)) {
    //     dataset.push({'y': d3.randomUniform(-10, 10)()})
    // }

    for (var i in d3.range(n)) {
        datasetExcite.push({'y': data.moods[i].excitedness})
        datasetHappy.push({'y': data.moods[i].happiness})
        meanExcite.push({'y': data['mean_excitedness']})
        meanHappy.push({'y': data['mean_happiness']})
    }

    console.log(meanExcite)

    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 200, bottom: 30, left: 200};
    var width = 900 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    // 5. X scale will use the index of our data
    var xScale = d3.scaleLinear()
        .domain([0, data.moods.length]) // input
        .range([0, width]); // output

    // 6. Y scale will use the randomly generate number
    var yScale = d3.scaleLinear()
        .domain([-10, 10]) // input
        .range([height, 0]); // output

    var svg = d3.select(id).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // 3. Call the x axis in a group tag
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height / 2 + ")")
        .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

    // 4. Call the y axis in a group tag
    svg.append("g")
        .attr("class", "y axis")
        // .attr("transform", "translate(" + width / 2 + ", 0)")
        .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

//    console.log(data.songdata);

    // var dayArray = [];
    // var excitedArray = [];
    // var counter = 0;
    // for (var i in userdata.songdata) {
    //     console.log(userdata.songdata[i]);
    //     dayArray.push(counter);
    //     excitedArray.push(userdata.songdata[i].excitedness);
    //     counter += 1;
    // }

    // console.log(dayArray);
    // console.log(excitedArray);

    // var line = d3.line()
    // .x(function(data) {return xScale(dayArray)})
    // .y(function(data) {return yScale(excitedArray)});

    var lineExcite = d3.line()
    .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
    .y(function(d) { return yScale(d.y); }) // set the y values for the line generator
    .curve(d3.curveMonotoneX) // apply smoothing to the line

    var lineHappy = d3.line()
    .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
    .y(function(d) { return yScale(d.y); }) // set the y values for the line generator
    .curve(d3.curveMonotoneX) // apply smoothing to the line

    svg.append("path")
        .data([datasetExcite])
        .attr("class", "line")
        .attr("id", "exciteLine")
        .attr("d", lineExcite);

    svg.append("path")
        .data([datasetHappy])
        .attr("class", "line")
        .attr("id", "happyLine")
        .attr("d", lineHappy);

    svg.append("path")
        .data([meanExcite])
        .attr("class", "line")
        .attr("id", "exciteMean")
        .attr("d", lineExcite);

    svg.append("path")
        .data([meanHappy])
        .attr("class", "line")
        .attr("id", "happyMean")
        .attr("d", lineHappy);




    // Handmade legend
    var legendY = 150
    svg.append("circle").attr("cx",width+30).attr("cy",legendY).attr("r", 6).attr("id", "exciteLegend")
    svg.append("circle").attr("cx",width+30).attr("cy",legendY + 30).attr("r", 6).attr("id", "happyLegend")
    svg.append("text").attr("x", width+50).attr("y", legendY).text("Excitedness").style("font-size", "15px").attr("alignment-baseline","middle")
    svg.append("text").attr("x", width+50).attr("y", legendY + 30).text("Happiness").style("font-size", "15px").attr("alignment-baseline","middle")
    svg.append("circle").attr("cx",width+30).attr("cy",legendY + 60).attr("r", 6).attr("id", "exciteLegendMean")
    svg.append("circle").attr("cx",width+30).attr("cy",legendY + 90).attr("r", 6).attr("id", "happyLegendMean")
    svg.append("text").attr("x", width+50).attr("y", legendY + 60).text("Mean excitedness").style("font-size", "15px").attr("alignment-baseline","middle")
    svg.append("text").attr("x", width+50).attr("y", legendY + 90).text("Mean happiness").style("font-size", "15px").attr("alignment-baseline","middle")

    // 12. Appends a circle for each datapoint 
    svg.selectAll(".excitedot")
    .data(datasetExcite)
    .enter().append("circle") // Uses the enter().append() method
    .attr("class", "excitedot") // Assign a class for styling
    .attr("cx", function(d, i) { return xScale(i) })
    .attr("cy", function(d) { return yScale(d.y) })
    .attr("r", 5)


    svg.selectAll(".happydot")
    .data(datasetHappy)
    .enter().append("circle") // Uses the enter().append() method
    .attr("class", "happydot") // Assign a class for styling
    .attr("cx", function(d, i) { return xScale(i) })
    .attr("cy", function(d) { return yScale(d.y) })
    .attr("r", 5)
    .on("mouseover", function(a, b, c) { 
            console.log(a) 
        this.attr('class', 'focus')
        })
    .on("mouseout", function() {  })


    // 12. Appends a circle for each datapoint
    // svg.selectAll(".dot")
    // .data(datasetExcite)
    // .enter().append("circle") // Uses the enter().append() method
    // .attr("class", "dot") // Assign a class for styling
    // .attr("cx", function(d, i) { return xScale(i) })
    // .attr("cy", function(d) { return yScale(d.y) })
    // .attr("r", 5)


    // svg.selectAll(".dot")
    // .data(datasetHappy)
    // .enter().append("circle") // Uses the enter().append() method
    // .attr("class", "dot") // Assign a class for styling
    // .attr("cx", function(d, i) { return xScale(i) })
    // .attr("cy", function(d) { return yScale(d.y) })
    // .attr("r", 5)
    // .on("mouseover", function(a, b, c) {
    //         console.log(a)
    //     this.attr('class', 'focus')
    //     })
    // .on("mouseout", function() {  })
}
