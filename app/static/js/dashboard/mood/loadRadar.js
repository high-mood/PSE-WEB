

function createRadarChart(userdata) {

  /* Radar chart design created by Nadieh Bremer - VisualCinnamon.com */
  var margin = {top: 100, right: 100, bottom: 100, left: 100},
    width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
    height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);


  var color = d3.scaleOrdinal().range(["#EDC951","#EDC951"])

  var radarChartOptions = {
    // w: width,
    // h: height,
    w: 500,
    h: 500,
    margin: margin,
    maxValue: 10,
    levels: 5,
    opacityArea: 0.1,
    roundStrokes: true,
    color: color
  };


  var finaldata = [];
  var song;
  for (i = 0; i < userdata.songs.length; i++) {

    song = {
      name : 'Song',
      axes : [
        {axis:"High Excitedness",value:userdata.songs[i].excitedness},
        {axis:"High Happiness",value:userdata.songs[i].happiness},
        {axis:"Low Excitedness",value:0.0},
        {axis:"Low Happiness",value:0.0}
      ]
    }
    finaldata.push(song);
  }

  let svg_radar1 = RadarChart(".radarChart", finaldata, radarChartOptions);
}

