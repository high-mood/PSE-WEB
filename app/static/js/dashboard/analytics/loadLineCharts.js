$('#lineSongs').hide()

function requestLineCharts() {
  var linechartRequest= new XMLHttpRequest()

  var metrics = "acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, valence";
  // console.log($('#songs-slider').data('slider'))//.getValue())//('values'));
  song_count = songsSliderObj.slider('getValue');

  // linechartRequest.open('GET', 'https://cors-anywhere.herokuapp.com/http://randomelements.nl/highmood/data/dummysonghistory.json', true)
  // linechartRequest.open('GET', 'http://localhost:5000/api/tracks/metrics/' + userid + '/' + metrics + '/' + song_count, true)
  linechartRequest.open('GET', 'http://localhost:5000/api/tracks/metrics/' + userid + '/' + song_count, true)
  linechartRequest.onload = function() {
    var alldata = JSON.parse(this.response)
    var userdata = alldata.resource

    if (linechartRequest.status >= 200 && linechartRequest.status < 400) {
      // lineGraph
      createLineGraphSongs(userdata,"lineSongs");
      // giveText(userdata,"lineGraphText");
    }
    else {
      document.getElementById("userwelcome").innerHTML = "Error retrieving data!"
    }
  }
  linechartRequest.send()


  var linechartDaysRequest = new XMLHttpRequest()

  // var metrics = "acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, valence";
  days = daysSliderObj.slider('getValue');
  console.log(days)
  // linechartDaysRequest.open('GET', 'https://cors-anywhere.herokuapp.com/http://randomelements.nl/highmood/data/api_days_dummy.json', true)
  linechartDaysRequest.open('GET', 'http://localhost:5000/api/user/mood/daily/' + userid + '/' + days, true)
  linechartDaysRequest.onload = function() {
    var alldata = JSON.parse(this.response)
    var userdata = alldata.resource

    if (linechartDaysRequest.status >= 200 && linechartDaysRequest.status < 400) {
      // lineGraph
      createLineGraphDays(userdata,"lineDays");
      // giveText(userdata,"lineGraphText");
    }
    else {
      document.getElementById("userwelcome").innerHTML = "Error retrieving data!"
    }
  }
  linechartDaysRequest.send()
}

requestLineCharts()

function toggleLineCharts(chartname) {
    if (chartname === 'lineDays') {
      $('#lineChartSelector').text("Days ")
      $('#lineChartSelector').append("<span class=\"caret\"></span>")
        $('#lineDays').show();
        $('#lineSongs').hide();
        $("#timeframe-slider-div").hide()
        $("#days-slider-div").show()
        $("#songs-slider-div").hide()
    }
    else if (chartname === 'lineSongs') {
      $('#lineChartSelector').text("Songs ")
      $('#lineChartSelector').append("<span class=\"caret\"></span>")
        $('#lineDays').hide();
        $('#lineSongs').show();
        $("#timeframe-slider-div").hide()
        $("#days-slider-div").hide()
        $("#songs-slider-div").show()
    }
}