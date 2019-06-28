/**
 * Discription.
 * 
 * @copyright 2019 Moodify (High-Mood)
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

/** Function to create a radarchart based off userdata
 * 
 * @param {*} userdata 
 */
function createRadarChart(userdata) {

  // Set chart margin
  var margin = {top: 100, right: 100, bottom: 100, left: 100},
    width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
    height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);

  var finalData = [];
  var song;
  var highestval = 0

  // Loop over user songs
  for (i = 0; i < userdata.songs.length; i++) {

    // Get highest absolute score, to be used to scale the chart
    if (Math.abs(userdata.songs[i].excitedness) > highestval) {
      highestval = Math.abs(userdata.songs[i].excitedness);
    }
    if (Math.abs(userdata.songs[i].happiness) > highestval) {
      highestval = Math.abs(userdata.songs[i].happiness);
    }

    // Create and push entry for current song to chart
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

  // Set radarchart styling options
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
    color: "#EDC951",
    labelFactor: 1.2
  };

  // Create radarchart
  let svg_radar1 = RadarChart(".radarChart", finalData, radarChartOptions);
}
