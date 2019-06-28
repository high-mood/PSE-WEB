$('#lineSongs').hide()
$('#barChart').hide()
analyticsDescription("days")

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