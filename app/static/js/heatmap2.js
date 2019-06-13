// Makes a heatmap with data in the format [{name:?,data0:?,data1:?},...]
function createHeatmap(divID, title, xMin, xMax, xSamples, xLabel, yMin, yMax, ySamples, yLabel, data) {
  // calculate variables
  var width = 500;
  var height = 500;
  var xDomainSize = xMax - xMin;
  var yDomainSize = yMax - yMin;
  var xSampleWidth = 8 * width / 10 / xSamples;
  var ySampleWidth = 8 * height / 10  / ySamples;

  // make svg in <div id=divID>
  var svg = d3.select("#" + divID).append("svg")
              .attr('width', width)
              .attr('height', height);

  // Convert data to a usable dataSet with the format [{x:?,y:?,size(),names:[?,...]},...].
  var dataSet = [];
  for (var x = 0; x < xSamples; x++) {
    var xMinReach = x * xDomainSize / xSamples + xMin;
    var xMaxReach = (x + 1) * xDomainSize / xSamples + xMin;
    for (var y = 0; y < ySamples; y++) {
      var dataPoint = {x:x,y:y,size:0,names:[]};
      var yMinReach = (ySamples - y - 1) * yDomainSize / ySamples + yMin;
      var yMaxReach = (ySamples - y) * yDomainSize / ySamples + yMin;
      // Find all conforming data for this dataPoint.
      var conformingDataNames = data.filter(function (data) {
        return (data.data0 >= xMinReach) && (data.data0 < xMaxReach) && (data.data1 >= yMinReach) && (data.data1 < yMaxReach);
      }).map(function(data) { return data.name; });
      dataPoint.size = conformingDataNames.length;
      dataPoint.names = conformingDataNames;
      dataSet.push(dataPoint);
    }
  }

  // Set colorScale with the data.
  var maxSize = d3.max(dataSet.map(function(data) { return data.size; }));
  var colorScale = d3.scaleLinear()
                           .domain([0, maxSize])
                           .range(['rgba(21,21,243,0.2)','rgba(243,21,21,0.8)']);


  // Add in squares for all dataPoints in dataSet.
  svg.selectAll('rect').data(dataSet)
    .enter().append('rect')
    .attr('fill', function (data) {
      if (data.size == 0) {
        return '#C3D4D6';
      } else {
        return colorScale(data.size);
      }
    })
    .attr('stroke', 'black')
    .attr('stroke-width', 0)
    .attr('width', 9 * xSampleWidth / 10)
    .attr('height', 9 * ySampleWidth / 10)
    .attr('x', function (data) {
      return data.x * xSampleWidth + width / 10 + xSampleWidth / 20;
    })
    .attr('y', function (data) {
      return data.y * ySampleWidth + height / 10 + ySampleWidth / 20;
    })
    .on("mouseover", function () {
      d3.select(this)
        .attr('stroke-width', 2);
    })
    .on("mouseout", function () {
      d3.select(this)
        .attr('stroke-width', 0);
    });


  // Add in axes.
  var xScale = d3.scaleLinear()
    .domain([xMin,xMax])
    .range([0,16 * width / 20]);
  var xAxis = d3.axisBottom()
    .scale(xScale)
    .ticks(d3.min([xSamples,20]));
  svg.append("g").call(xAxis)
    .attr("transform","translate(" + width / 10 + "," + 18.75 * height / 20 + ")");

  var yScale = d3.scaleLinear()
    .domain([yMin,yMax])
    .range([16 * height / 20, 0]);
  var yAxis = d3.axisLeft()
    .scale(yScale)
    .ticks(d3.min([ySamples,20]));
  svg.append("g").call(yAxis)
    .attr("transform","translate(" + width / 15 + "," + height / 10 + ")");

  // add labels on the axes
  svg.append("g")
    .attr("text-anchor", "middle")
    .attr("transform", "translate(" + 3 + "," + height / 2 + ")rotate(" + 90 + "," + 0 + "," + 0 + ")")
    .append("text")
    .text(xLabel);

  svg.append("g")
      .attr("text-anchor", "middle")
      .attr("transform", "translate(" + width / 2 + "," + (9.9 * height / 10) + ")")
      .append("text")
      .text(yLabel);

  // Add a title at the top.
  svg.append("g")
    .attr("text-anchor", "middle")
    .attr("transform", "translate(" + (width / 2) + "," + height / 20 + ")")
    .append("text")
    .text(title)
}
