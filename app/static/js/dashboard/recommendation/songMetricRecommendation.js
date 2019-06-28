/**
* Controles the song recommendation section of the web page.
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

/**
 * Onclick handler that changes the page when a different metic is selected. 
 * 
 * @param {string} metricName The selected metric
 */
function toggleMetric(metricName) {
  // Display name of metric.
  var themes = ['dance', 'karaoke', 'study'];
  var formattedstring = ""
  if (metricName != 'dance') {
    formattedstring = metricName.charAt(0).toUpperCase() + metricName.slice(1) + " ";
  } else {
    formattedstring = "Party ";
  }

  // Update button texts.
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

  // Request the recommendations from API
  var request = new XMLHttpRequest;
<<<<<<< HEAD
  request.open('GET', 'http://pse-ssh.diallom.com:5000/api/tracks/recommendation/' + userid + '/' + metricName, true);
=======
  request.open('GET', 'http://localhost:5000/api/tracks/recommendation/' + userid + '/' + metricName, true)
>>>>>>> cf86ab68cc319b665f29ff764d136d6c9ce74a65
  request.onload = function() {
    var alldata = JSON.parse(this.response);
    if (request.status >= 200 && request.status < 400) {
      // Display the data.
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

/**
 * Fill the recomandations div's with recommandations.
 * 
 * @param {list} userData Contains dicts with recommended songs
 */
function fillRecommendations(userData) {
  // Fill 5 divs max, less if there is no data.
  for(var index = 0; index < Math.min(5, userData.length); index++) {
    div = $('#rec' + index);
    div.empty();
    trackId = "https://open.spotify.com/embed/track/";
    trackId += userData[index].songid;

    content = '<iframe class="song-template" src="' + trackId + '" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>';
    div.append(content);
  }
}

// Ensures that default 
toggleMetric('neutral');
