/**
 * Loads the line charts for the analytics section.
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

$('#lineSongs').hide()
$('#barChart').hide()
analyticsDescription("days")

/**
 * @summary Sends a request to the API to get the data for the line charts.
 *
 * @param {Boolean} retriggered
 */
function requestLineCharts(retriggered) {
  var linechartRequest= new XMLHttpRequest()

  var metrics = "acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, valence";
  song_count = songsSliderObj.slider('getValue');

  linechartRequest.open('GET', 'http://pse-ssh.diallom.com:5000/api/tracks/metrics/' + userid + '/' + song_count, true)
  linechartRequest.onload = function() {
    var alldata = JSON.parse(this.response)
    var userdata = alldata.resource

    if (linechartRequest.status >= 200 && linechartRequest.status < 400) {
      // lineGraph
      createLineGraphSongs(userdata,"lineSongs", retriggered);
    }
    else {
      document.getElementById("userwelcome").innerHTML = "Error retrieving data!"
    }
  }
  linechartRequest.send()


  var linechartDaysRequest = new XMLHttpRequest()

  days = daysSliderObj.slider('getValue');
  linechartDaysRequest.open('GET', 'http://pse-ssh.diallom.com:5000/api/user/mood/daily/' + userid + '/' + days, true)
  linechartDaysRequest.onload = function() {
    var alldata = JSON.parse(this.response)
    var userdata = alldata.resource

    if (linechartDaysRequest.status >= 200 && linechartDaysRequest.status < 400) {
      // lineGraph
      createLineGraphDays(userdata,"lineDays", retriggered);
    }
    else {
      document.getElementById("userwelcome").innerHTML = "Error retrieving data!"
    }
  }
  linechartDaysRequest.send()



  var barchartRequest = new XMLHttpRequest()

  var start, end;
  [start, end] = timeframeSliderObj.slider('getValue');

  barchartRequest.open('GET', 'http://pse-ssh.diallom.com:5000/api/user/mood/hourly/' + userid + '/' + start + '/' + end, true)
  barchartRequest.onload = function() {
    var alldata = JSON.parse(this.response)
    var userdata = alldata.resource

    if (barchartRequest.status >= 200 && barchartRequest.status < 400) {
      // lineGraph
      createBarChart("barChart",start,end,userdata["hours"]);
    }
    else {
      document.getElementById("userwelcome").innerHTML = "Error retrieving data!"
    }
  }
  barchartRequest.send()
}

requestLineCharts(false)

/**
 * @summary Toggles the charts based on the chartname to switch to.
 *
 * @param {String} chartname
 */
function toggleLineCharts(chartname) {
    if (chartname === 'lineDays') {
      $('#lineChartSelector').text("Days ")
      $('#lineChartSelector').append("<span class=\"caret\"></span>")
      $('#lineDays').show();
      $('#lineSongs').hide();
      $('#barChart').hide();
      $("#timeframe-slider-div").hide()
      $("#days-slider-div").show()
      $("#songs-slider-div").hide()
      $("#linechart-buttons").show()
      analyticsDescription("days")
      showButtonsTimeframe();
    }
    else if (chartname === 'lineSongs') {
      $('#lineChartSelector').text("Songs ")
      $('#lineChartSelector').append("<span class=\"caret\"></span>")
      $('#lineDays').hide();
      $('#lineSongs').show();
      $('#barChart').hide();
      $("#timeframe-slider-div").hide()
      $("#days-slider-div").hide()
      $("#songs-slider-div").show()
      $("#linechart-buttons").show()
      analyticsDescription("songs");
      showButtonsTimeframe();
    }
    else if (chartname === 'barChart') {
      $('#lineChartSelector').text("Hourly ")
      $('#lineChartSelector').append("<span class=\"caret\"></span>")
      $('#lineDays').hide();
      $('#lineSongs').hide();
      $('#barChart').show();
      $("#timeframe-slider-div").show();
      $("#days-slider-div").hide();
      $("#songs-slider-div").hide();
      analyticsDescription("bar");
      hideButtonsTimeframe();
    }
}


/**
 * @summary Hides the buttons for the timeframe chart except for happiness and excitedness.
 *
 */
function hideButtonsTimeframe() {
  var buttonNames = ["excitedness", "happiness", "acousticness", "danceability", 
  "energy", "instrumentalness", "liveness", "speechiness", 
  "tempo", "valence"];

  for (var i in buttonNames) {
    if (buttonNames[i] == "excitedness" || buttonNames[i] == "happiness") {
      $(`#${buttonNames[i]}`).show()
      $(`#${buttonNames[i]}`).attr("disabled", true)
    }
    else {
      $(`#${buttonNames[i]}`).hide()
    }

  }
}

/** @summary Build and show the buttons for metric selection   */
function showButtonsTimeframe() {
  var buttonNames = ["excitedness", "happiness", "acousticness", "danceability", 
  "energy", "instrumentalness", "liveness", "speechiness", 
  "tempo", "valence"];
  for (var i in buttonNames) {
    if (buttonNames[i] == "excitedness" || buttonNames[i] == "happiness") {
      $(`#${buttonNames[i]}`).show()
      $(`#${buttonNames[i]}`).attr("disabled", false)
    }
    else {
      $(`#${buttonNames[i]}`).show()
    }
  }
}