function createSongRecommendationWidget(userid) {

  var request = new XMLHttpRequest()

  // request.open('GET', 'https://cors-anywhere.herokuapp.com/http://randomelements.nl/highmood/data/dummysonghistory.json', true)
  request.open('GET', 'http://pse-ssh.diallom.com:5000/api/tracks/history/' + userid + '/0', true)

  request.onload = function() {
    var alldata = JSON.parse(this.response)
    var userdata = alldata.resource


    if (request.status >= 200 && request.status < 400) {

      var songWidgetContainer = document.getElementById('Song-Recommendation');

      var form = document.createElement('form')

      songWidgetContainer.appendChild(form);


      var length = userdata.songs.length;

      if (length >= 5) {
        length = 5;
      }

      for (var i = 0; i < length; i++) {
        var songdiv = document.createElement('div')
        songdiv.classList.add('songdiv');
        songdiv.id = userdata.songs[i].songid;

        var songid = userdata.songs[i].songid;

        var btn = document.createElement("BUTTON");
        btn.innerHTML = "Select";
        btn.setAttribute("type","button");
        btn.onclick = function(songid) { showSong(songid); };
        btn.classList.add('SongRecButton');
        songdiv.appendChild(btn);

        var ifrm = document.createElement("iframe");
        ifrm.setAttribute("src", "https://open.spotify.com/embed/track/" + userdata.songs[i].songid);
        ifrm.setAttribute("align","left");
        ifrm.style.width = "300px";
        ifrm.style.height = "80px";


        songdiv.appendChild(ifrm);
        form.appendChild(songdiv)


      }


    }
  }
  request.send()

}

function showSong(clickevent) {
  var songid = [clickevent.path[0].parentElement.id];


  var songdivs = document.getElementsByClassName("songdiv");

  for (var i = 0; i < songdivs.length; i++) {

    if (songdivs[i].childNodes.length > 2) {

      for (var j = 2; j < songdivs[i].childNodes.length; j++) {
        songdivs[i].removeChild(songdivs[i].childNodes[j]);
      }
    }

  }

  var request = new XMLHttpRequest()

  request.open('GET', 'http://pse-ssh.diallom.com:5000/api/tracks/recommendation/' + userid + '/' + songid + '/0.0/0.0', true)
  // http://pse-ssh.diallom.com:5000/api/tracks/recommendation/snipy12/0LtOwyZoSNZKJWHqjzADpW/0.0/0.0
  request.onload = function() {
    var alldata = JSON.parse(this.response)
    var userdata = alldata.resource

    if (request.status >= 200 && request.status < 400) {

      songdivs = document.getElementsByClassName("songdiv");

      for (var i = 0; i < songdivs.length; i++) {


        var ifrm = document.createElement("iframe");
        ifrm.setAttribute("src", "https://open.spotify.com/embed/track/" + userdata.recommendations[i].songid);
        ifrm.setAttribute("align","left");
        ifrm.style.width = "300px";
        ifrm.style.height = "80px";

        songdivs[i].appendChild(ifrm)
      }

    }
  }
  request.send()

}
