function toggleMetric(metricName) {
    if (metricName == 'dance') {metricName = 'party'};
    var themes = ['party', 'karaoke', 'study'];
    var formattedstring = metricName.charAt(0).toUpperCase() + metricName.slice(1) + " ";
    if (themes.includes(metricName)) {
	document.getElementById("moodbutton").innerHTML =
	    "Mood " + "<span class=\"caret\"></span>";
	document.getElementById("themebutton").innerHTML =
	    formattedstring + "<span class=\"caret\"></span>";
    } else {
	document.getElementById("moodbutton").innerHTML =
	    formattedstring + "<span class=\"caret\"></span>";
	document.getElementById("themebutton").innerHTML =
	    "Theme " + "<span class=\"caret\"></span>";
    }
    
  var request = new XMLHttpRequest;
  request.open('GET', 'http://pse-ssh.diallom.com:5000/api/tracks/recommendation/' + userid + '/' + metricName, true)
  request.onload = function() {
    var alldata = JSON.parse(this.response);
    if (request.status >= 200 && request.status < 400) {
      var userdata = alldata.resource.recommendations;
      fillRecommendations(userdata);
    } else {
      for(var index = 0; index < 5; index++) {
        div = $('rec' + index);
        div.empty();
        div.append("Error loading the content");
      }
    }
  }
  request.send()
}

function fillRecommendations(userData) {
  for(var index = 0; index < Math.min(5, userData.length); index++) {
    div = $('#rec' + index);
    div.empty();
    trackId = "https://open.spotify.com/embed/track/";
    trackId += userData[index].songid;

    content = '<iframe class="song-template" src="' + trackId + '" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>';
    div.append(content);
  }
}

toggleMetric('neutral');
