// Function to create the radarchart from the userdata.
function createRadarChart(userdata) {

  /* Radar chart design created by Nadieh Bremer - VisualCinnamon.com */
  var margin = {top: 100, right: 100, bottom: 100, left: 100},
    width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
    height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);

  var color = d3.scaleOrdinal().range(["#EDC951","#EDC951"])

  var finalData = [];
  var song;
  var highestval = 0
  for (i = 0; i < userdata.songs.length; i++) {
    if (Math.abs(userdata.songs[i].excitedness) > highestval) {
      highestval = Math.abs(userdata.songs[i].excitedness);
    }

    if (Math.abs(userdata.songs[i].happiness) > highestval) {
      highestval = Math.abs(userdata.songs[i].happiness);
    }

    song = {
      name : 'Song',
      axes : [
        {axis:"High Excitedness",value:userdata.songs[i].excitedness},
        {axis:"High Happiness",value:userdata.songs[i].happiness},
        {axis:"Low Excitedness",value:0.0},
        {axis:"Low Happiness",value:0.0}
      ]
    }
    finalData.push(song);
  }

  var radarChartOptions = {
    w: 500,
    h: 500,
    margin: margin,
    factorlegend: 0,
    maxValue: Math.floor(highestval),
    levels: 0,
    opacityArea: 0.1,
    axisLine: true,
    roundStrokes: true,
    color: color,
    labelFactor: 1.2
  };

  let svg_radar1 = RadarChart(".radarChart", finalData, radarChartOptions);
}
