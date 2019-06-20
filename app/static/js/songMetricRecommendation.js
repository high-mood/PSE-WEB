function MakeNewSongMetricRec(targetDiv,metricName) {
  var userid = document.getElementById("username").textContent;

  var request = new XMLHttpRequest
  request.open('GET', 'http://localhost:5000/api/tracks/recommendation/' + userid + '/' + metricName, true)
  request.onload = function() {
    var alldata = JSON.parse(this.response)
    if (request.status >= 200 && request.status < 400) {
      var userdata = alldata.resource.recommendations
      createSongRecommendationsPlayer(targetDiv,userdata);
    } else {
      targetDiv.innerHTML="Error loading the content"
    }
  }
  request.send()
}

function createSongRecommendationsPlayer(mainDivId,songs) {
  console.log(songs)
  mainDiv = document.getElementById(mainDivId);
  // clear former songs
  mainDiv.innerHTML = "";

  // create header with labels
  songLabelBar = document.createElement('div');
  songLabelBar.setAttribute("class","songPlayerBar");
  mainDiv.appendChild(songLabelBar);

  playerDiv = document.createElement('div');
  playerDiv.setAttribute("style","width: 50%; height: 100%; float: left;")
  playerDiv.appendChild(document.createTextNode("recommendation"));
  songLabelBar.appendChild(playerDiv);

  excitementDiv = document.createElement('div');
  excitementDiv.setAttribute("style","width: 25%; height: 100%; float: left;")
  excitementDiv.appendChild(document.createTextNode("excitedness"));
  songLabelBar.appendChild(excitementDiv);

  happinessDiv = document.createElement('div');
  happinessDiv.setAttribute("style","width: 25%; height: 100%Responses; float: left;")
  happinessDiv.appendChild(document.createTextNode("happiness"));
  songLabelBar.appendChild(happinessDiv);

  // create song elements
  for (i=0;i<5;i++) {
    songPlayerBar = document.createElement('div');
    songPlayerBar.setAttribute("class","songPlayerBar");
    mainDiv.appendChild(songPlayerBar);

    // create iframesongId
    spotifyPlayer = document.createElement('iframe');
    spotifyPlayer.setAttribute("src","https://open.spotify.com/embed/track/" + songs[i].songid);
    spotifyPlayer.setAttribute("frameborder","0");
    spotifyPlayer.setAttribute("allowtransparency","true");
    spotifyPlayer.setAttribute("allow","encrypted-media");
    spotifyPlayer.setAttribute("style","width: 50%; height: 100%; float: left;")
    songPlayerBar.appendChild(spotifyPlayer);

    // show metrics
    excitementDiv = document.createElement('div');
    excitementDiv.setAttribute("style","width: 25%; height: 100%; float: left;")
    excitementDiv.appendChild(document.createTextNode(songs[i].excitedness));
    songPlayerBar.appendChild(excitementDiv);

    happinessDiv = document.createElement('div');
    happinessDiv.setAttribute("style","width: 25%; height: 100%; float: left;")
    happinessDiv.appendChild(document.createTextNode(songs[i].happiness));
    songPlayerBar.appendChild(happinessDiv);
  }
}

function createSongRecommendationElement(mainDivId) {
  mainDiv = document.getElementById(mainDivId);

  // 1 make metric selection Bar
  metricBar = document.createElement('div');
  metricBar.setAttribute("class","songMetricBar");
  mainDiv.appendChild(metricBar);

  // 1.1 make options

  // 1.1.1 metric
  metricsDiv = document.createElement('div');
  metricBar.appendChild(metricsDiv);

  metricsHeaderDiv = document.createElement('div');
  metricsHeaderDiv.setAttribute("class","metricHeader");
  metricsHeaderDiv.appendChild(document.createTextNode("By metric"));
  metricsDiv.appendChild(metricsHeaderDiv);

  var metrics = ["dancability","energy","metric2","metric3"];

  for (i=0;i<4;i++) {
    newDiv = document.createElement('div');
    newDiv.setAttribute("class","metricElement");
    newDiv.setAttribute("onclick","MakeNewSongMetricRec('songMetricRecPlayer','" + metrics[i] + "')");
    newDiv.appendChild(document.createTextNode(metrics[i]));
    metricsDiv.appendChild(newDiv);
  }

  // 1.1.2 mood
  moodsDiv = document.createElement('div');
  metricBar.appendChild(moodsDiv);

  moodsHeaderDiv = document.createElement('div');
  moodsHeaderDiv.setAttribute("class","metricHeader");
  moodsHeaderDiv.appendChild(document.createTextNode("By mood"));
  moodsDiv.appendChild(moodsHeaderDiv);

  var moods = ["sad","angry","excited","mellow"];

  for (i=0;i<4;i++) {
    newDiv = document.createElement('div');
    newDiv.setAttribute("class","metricElement");
    newDiv.setAttribute("onclick","MakeNewSongMetricRec('songMetricRecPlayer','" + moods[i] + "')");
    newDiv.appendChild(document.createTextNode(moods[i]));
    moodsDiv.appendChild(newDiv);
  }

  // 2 make div for eventual songs
  songsBar = document.createElement('div');
  songsBar.setAttribute("class","songRecBar");
  songsBar.setAttribute("id","songMetricRecPlayer");
  mainDiv.appendChild(songsBar);


  // todo make placeholder for when no 

  var songs = [{songId:"29bFmmZdmYstqJeEOweJoI",excitedness:100,happiness:100},{songId:"29bFmmZdmYstqJeEOweJoI",excitedness:100,happiness:100},{songId:"29bFmmZdmYstqJeEOweJoI",excitedness:100,happiness:100},{songId:"29bFmmZdmYstqJeEOweJoI",excitedness:100,happiness:100},{songId:"29bFmmZdmYstqJeEOweJoI",excitedness:100,happiness:100}]

  createSongRecommendationsPlayer("songMetricRecPlayer",songs);
}