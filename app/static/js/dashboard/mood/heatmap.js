// Transform data so heatmap can use it.
function createHeatmapData(userData, xMin, xMax, yMin, yMax, xSamples, ySamples, xDomainSize, yDomainSize) {
  // 0. Get all data needed from the songs.
  songData = []
  for (var i in d3.range(userData.songs.length)) {
    var song = userData.songs[i];
    songData.push({name:song.name,data0:song.excitedness,data1:song.happiness});
  }

  // 1. Convert songData to dataSet usable in the heatmap.
  var dataSet = [];
  for (var x = 0; x < xSamples; x++) {
    var xMeanReach = (x + 0.5) * xDomainSize / xSamples + xMin;
    for (var y = 0; y < ySamples; y++) {
      var dataPoint = {x:x,y:y,size:0};
      var yMeanReach = (y + 0.5) * yDomainSize / ySamples + yMin;
      // Find all conforming data for this dataPoint.
      // var conformingDataNames = songData.filter(function (songData) {
      //   return (songData.data0 - xMeanReach) ** 2 + (songData.data1 - yMeanReach) ** 2 < 9;
      // }).map(function(songData) { return songData.name; });
      // dataPoint.size = conformingDataNames.length;
      for( var i = 0; i < songData.length; i++) {
        dataPoint.size += 1 / (1 + (((songData[i].data0 - xMeanReach) ** 2 + (songData[i].data1 - yMeanReach) ** 2)) ** 0.5)
      }


      dataSet.push(dataPoint);
    }
  }

  return dataSet
}

// Makes a heatmap svg element.
function createHeatmap(divID, title, xMin, xMax, xSamples, xLabel, yMin, yMax, ySamples, yLabel, userData) {

  // 0. Set colors for the colorScale
  var lowDataColor = 'black';
  var highDataColor = 'red';

  // 1. Calculate variables for the size of the elements.
  var width = 500;
  var height = 500;
  var xDomainSize = xMax - xMin;
  var yDomainSize = yMax - yMin;
  var xSampleWidth = 8 * width / 10 / xSamples;
  var ySampleWidth = 8 * height / 10  / ySamples;

  // 2. Convert data to a usable dataSet with the format [{x:?,y:?,size(),names:[?,...]},...].
  var dataSet = createHeatmapData(userData, xMin, xMax, yMin, yMax, xSamples, ySamples, xDomainSize, yDomainSize);

  // 3. Set colorScale for the data.
  var maxSize = d3.max(dataSet.map(function(data) { return data.size; })) + 1;
  var minSize = d3.min(dataSet.map(function(data) { return data.size; }));
  var colorScale = d3.scaleLinear().domain([minSize, maxSize]).range([lowDataColor, highDataColor]);

  // 4. Set scales for x and y direction
  var xScale = d3.scaleLinear()
                 .domain([xMin,xMax])
                 .range([0,16 * width / 20]);
  var yScale = d3.scaleLinear()
                 .domain([yMin,yMax])
                 .range([16 * height / 20, 0]);

  // 5. Make svg in the targeted div.
  var svg = d3.select("#" + divID).append("svg")
              .attr('width', "100%")
              .attr('height', "100%")
              .attr("viewBox","0 0 500 505")
              .attr("preserveAspectRatio","xMidYMid meet");

  // 5.1. Add in squares for all dataPoints in dataSet.
  svg.selectAll('rect').data(dataSet)
    .enter().append('rect')
    .attr('fill', function (data) {
      return colorScale(data.size);
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


  // 5.2.1 Add in axes.
  var xAxis = d3.axisBottom()
    .scale(xScale)
    .ticks(d3.min([xSamples,20]));
  svg.append("g")
    .attr("class","heatmapAxis")
    .call(xAxis)
      .attr("transform","translate(" + width / 10 + "," + 18.75 * height / 20 + ")");
  var yAxis = d3.axisLeft()
    .scale(yScale)
    .ticks(d3.min([ySamples,20]));
  svg.append("g")
    .attr("class","heatmapAxis")
    .call(yAxis)
      .attr("transform","translate(" + width / 15 + "," + height / 10 + ")");

  // 5.2.2 Add labels on the axes.
  svg.append("g")
    .attr("text-anchor", "middle")
    .attr("transform", "translate(" + 3 + "," + height / 2 + ")rotate(" + 90 + "," + 0 + "," + 0 + ")")
    .attr("fill","#ffffff")
    .append("text")
    .text(xLabel);
  svg.append("g")
    .attr("text-anchor", "middle")
    .attr("transform", "translate(" + width / 2.05 + "," + height + ")")
    .attr("fill","#ffffff")
    .append("text")
    .text(yLabel);

  // 5.3. Add a title at the top.
  svg.append("g")
    .attr("text-anchor", "middle")
    .attr("transform", "translate(" + (width / 2) + "," + height / 20 + ")")
    .attr("fill","#ffffff")
    .append("text")
    .text(title)
}
