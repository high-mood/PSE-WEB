

function createRadarChart() {

  /* Radar chart design created by Nadieh Bremer - VisualCinnamon.com */
  var margin = {top: 100, right: 100, bottom: 100, left: 100},
    width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
    height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);

  var color = d3.scale.ordinal()
    .range(["#EDC951","#EDC951"]);

  var radarChartOptions = {
    w: width,
    h: height,
    margin: margin,
    maxValue: 10,
    levels: 5,
    opacityArea: 0.1,
    roundStrokes: true,
    color: color
  };

  var request = new XMLHttpRequest()
  // request.setRequestHeader('Access-Control-Allow-Headers', '*');

  request.open('GET', 'https://cors-anywhere.herokuapp.com/http://randomelements.nl/highmood/data/dummydata.json', true)
  request.onload = function() {
    // Begin accessing JSON data here
    var userdata = JSON.parse(this.response)

    if (request.status >= 200 && request.status < 400) {

      document.title = userdata.username + "\'s  Mood";
      var x = document.getElementById("userwelcome").innerHTML = "Welcome " + userdata.username + ", here's your mood";

      var finaldata = [];
      var song;
      for (i = 0; i < userdata.songs; i++) {
        song = [
                {axis:"High Excitedness",value:userdata.songdata[i].excitedness},
                {axis:"High Happiness",value:userdata.songdata[i].happiness},
                {axis:"Low Excitedness",value:0.0},
                {axis:"Low Happiness",value:0.0}
                ]
        finaldata.push(song);
      }
      //Call function to draw the Radar chart
      RadarChart(".radarChart", finaldata, radarChartOptions);
    }
  }
  request.send()

}
