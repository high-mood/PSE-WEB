/* global $, document*/

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

      var form = document.createElement('form');
      form.setAttribute("class", "form-signin");
      form.setAttribute("action", "/signUp");
      form.setAttribute("method", "post");
      form.setAttribute("role", "form");

      var input = document.createElement('input');
      input.setAttribute("type", "email");
      input.setAttribute("name", "username");
      input.setAttribute("class", "form-control");

      var button = document.createElement('button');
      button.setAttribute("type", "button");
      // button.innerHTML = "Hallo";





      form.appendChild(input);
      form.appendChild(button);

      songWidgetContainer.appendChild(form);

      for (var i = 0; i < userdata.songs.length; i++) {
//        console.log(userdata.songs[i].songid);

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

        // <form class="form-signin" action="/signUp" method="post" role="form">
        //     <input type="email" name="username" class="form-control">
        //     <button type="button">Register </button>
        // </form>


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
//  console.log(songid);

  // alert(songid);
}

//$(function() {
//    $('button').click(function() {
//        $.ajax({
//            url: '/sendSong',
//            data: $('form').serialize(),
//            type: 'POST',
//            success: function(response) {
//                console.log(response);
//            },
//            error: function(error) {
//                console.log(error);
//            }
//        });
//    });
//});
