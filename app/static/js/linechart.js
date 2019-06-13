// Code by Gord Lea: https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89

function lineGraph(userdata, id) {

    console.log(userdata);

    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 20, bottom: 30, left: 50};
    var width = 500 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    // number of data points
    var n = 20

    console.log(data)
    // 5. X scale will use the index of our data
    var xScale = d3.scaleLinear()
        .domain([0, 20]) // input
        .range([0, width]); // output

    // 6. Y scale will use the randomly generate number 
    var yScale = d3.scaleLinear()
        .domain([-10, 10]) // input 
        .range([height, 0]); // output 

    var svg = d3.select(".linegraph").append("svg")
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

    console.log(data.songdata);

    var dayArray = [];
    var excitedArray = [];
    var counter = 0;
    for (var i in userdata.songdata) {
        console.log(userdata.songdata[i]);
        dayArray.push(counter);
        excitedArray.push(userdata.songdata[i].excitedness);
        counter += 1;
    }

    console.log(dayArray);
    console.log(excitedArray);

    var line = d3.line()
        .x(function(data) {return xScale(dayArray)})
        .y(function(data) {return yScale(excitedArray)});

    svg.append("path")
        .data([data.songdata])
        .attr("class", "line")
        .attr("d", line);
}

