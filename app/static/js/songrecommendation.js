function createSongRecommendationWidget(userid) {

  var request = new XMLHttpRequest()

  request.open('GET', 'https://cors-anywhere.herokuapp.com/http://randomelements.nl/highmood/data/dummysonghistory.json', true)
  // request.open('GET', 'http://localhost:5000/api/mood/' + userid + '/beginning%20of%20time/now', true)
  request.onload = function() {
    var alldata = JSON.parse(this.response)
    var userdata = alldata.resource


    if (request.status >= 200 && request.status < 400) {
      // console.log(userdata);

      var songWidgetContainer = document.getElementById('Song-Recommendation');

      var form = document.createElement('form')

      songWidgetContainer.appendChild(form);

      for (var i = 0; i < userdata.songs.length; i++) {
        console.log(userdata.songs[i].songid);

        var songdiv = document.createElement('div')
        songdiv.classList.add('songdiv');
        songdiv.id = userdata.songs[i].songid;

        // songdiv.onclick = function() { alert('hallo'); };
        // songdiv.onclick = showSong(userdata.songs[i].songid);
        //
        // var radioHtml = '<input type="radio" name="' + userdata.songs[i].name + '" value="' + userdata.songs[i].songid+ '"';
        // radioHtml += '/>';
        //
        // var radiobutton = document.createElement("INPUT");
        // radiobutton.setAttribute("type", "radio");
        // radiobutton.setAttribute("value", userdata.songs[i].songid)

        var songid = userdata.songs[i].songid;

        var btn = document.createElement("BUTTON");
        btn.innerHTML = "Select";
        // btn.onclick = showSong("hallo");
        btn.setAttribute("type","button");
        // btn.setAttribute("onclick","showSong(" + userdata.songs[i].songid + ")");
        btn.onclick = function(songid) { showSong(songid); };
        // btn.addEventListener("click", showSong("hallo"));
        btn.classList.add('SongRecButton');
        songdiv.appendChild(btn);



        var ifrm = document.createElement("iframe");
        ifrm.setAttribute("src", "https://open.spotify.com/embed/track/" + userdata.songs[i].songid);
        ifrm.setAttribute("align","left");
        ifrm.style.width = "300px";
        ifrm.style.height = "80px";



        // form.appendChild(radiobutton);
        songdiv.appendChild(ifrm);


        // songdiv.innerHTML = radioHtml;
        form.appendChild(songdiv)
        // form.appendChild('<br>')
        // form.innerHTML = radioHtml;
        // form.appendChild(radioHtml);
      }


    }
  }
  request.send()

}

function showSong(clickevent) {
  var songid = [clickevent.path[0].parentElement.id];
  console.log(songid);

  // alert(songid);
}
