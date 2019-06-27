var songiddict = {};

var request = new XMLHttpRequest()
// request.open('GET', 'https://cors-anywhere.herokuapp.com/http://randomelements.nl/highmood/data/dummysonghistory.json', true)
request.open('GET', 'https://cors-anywhere.herokuapp.com/http://pse-ssh.diallom.com:5000/api/tracks/history/' + "snipy12" + '/0', true)
request.onload = function() {

    if (request.status >= 200 && request.status < 400) {
        var alldata = JSON.parse(this.response);
        var userdata = alldata.resource;
	var tracklist = document.getElementById('tracklist');
        globaluserdata = userdata;
        var songWidgetContainer = document.getElementById('song_history');
        var form = document.createElement('form')

        songWidgetContainer.appendChild(form);
	
        var length = userdata.songs.length;
	
        if (length > 20) { length = 20; }
	
        for (var i = 0; i < length; i++) {
	    
            var song = userdata.songs[i];
            var songdiv = document.createElement('div');
            songdiv.classList.add('songdiv');
	   	      
            var songid = userdata.songs[i].songid;
            songdiv.id = songid;
	    
            songiddict[songid] = song;

            var btn = document.createElement("BUTTON");
            btn.innerHTML = "Select";
            btn.setAttribute("type","button");
            btn.onclick = function(songid) {createSongInfoTool(songid); };
            btn.classList.add('SongRecButton');
            songdiv.appendChild(btn);

            var ifrm = document.createElement("iframe");
            ifrm.setAttribute("src", "https://open.spotify.com/embed/track/" + userdata.songs[i].songid);
            ifrm.setAttribute("align","right");
            ifrm.style.width = "300px";
            ifrm.style.height = "80px";

            songdiv.appendChild(ifrm);
            form.appendChild(songdiv);
	    tracklist.style.width = ifrm.getAttribute("width") + btn.getAttribute("width")
        }
          // createSongInfoTool(userdata.songs[0]);
    }
}
request.send()

function createSongInfoTool(clickevent) {

    var songid = clickevent.path[0].parentElement.id;
    
    var song = songiddict[songid];

        // var songname = document.getElementById('songname');
        // var par = document.createElement("p");
        //
        // var text = document.createTextNode(song.name);
        // par.style.margin = "0px";
        // par.appendChild(text);
        // songname.appendChild(par);

    var songname = document.getElementById('songdisplayname')
    songname.innerHTML = song.name;

    var happiness_slider = document.getElementById("happiness_slider")
    var happiness_slider_text = document.getElementById("happiness_slider_text")
    var happiness_percentage = (song.happiness + 10) * 5
    happiness_slider.value = happiness_percentage;
    happiness_slider_text.innerHTML = "Happiness:\n" + Math.trunc(happiness_percentage) + "%";


    var excitedness_slider = document.getElementById("excitedness_slider")
    var excitedness_slider_text = document.getElementById("excitedness_slider_text")
    var excitedness_percentage = (song.excitedness + 10) * 5
    excitedness_slider.value = excitedness_percentage;
    excitedness_slider_text.innerHTML = "Excitedness:\n" + Math.trunc(excitedness_percentage) + "%";

        // songInfoContainer.appendChild(div);
};



// TODO  set to actual song feedbacl
function resetFeedback(event) {
    var value = 50;
    document.getElementById("happiness_slider").value = value;
    var text = document.getElementById("happiness_slider_text");
    text.textContent = value + "%";

    document.getElementById("excitedness_slider").value = value;
    var text = document.getElementById("excitedness_slider_text");
    text.textContent = value + "%";
}

// TODO call actual api with actual username
function sendFeedback(event) {
    var userid = "sinpy12";
    var happiness = document.getElementById("happiness_slider").value;
    var excitedness = document.getElementById("excitedness_slider").value;
    var uri = "http://localhost:5000/api/songs/mood/" + userid;
    var songid = "";

    var data = {
        "songid": songid,
        "excitedness": excitedness,
        "happiness": happiness
    };
    var request = new XMLHttpRequest();
    request.open("POST", uri, true);
    request.setRequestHeader("Content-Type", 'application/json');
    request.setRequestHeader("Access-Control-Allow-Origin", 'localhost:4000');
    request.send(JSON.stringify(data));
}

var song_history = document.querySelector("#song_history");
var tracklist = document.querySelector("#tracklist");

document.getElementById("happiness_slider").oninput = function() {
    var text = document.getElementById("happiness_slider_text");
    text.textContent = this.value + "%";
};

document.getElementById("excitedness_slider").oninput = function() {
    var text = document.getElementById("excitedness_slider_text");
    text.textContent = this.value + "%";
};


var resetButton = document.getElementById("reset_feedback");
resetButton.addEventListener("click", resetFeedback);

var sendFeedbackBackButton = document.getElementById("send_feedback");
sendFeedbackBackButton.addEventListener("click", sendFeedback);

