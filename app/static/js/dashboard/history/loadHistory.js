/* loadHistory.js
 *
 * This file contains javascript code to properly render the 'Review' section.
 *
 *
 * This file defines JQuery UI slider objects used in the section 'Analytics'.
 *
 *     This file contains the structure of the playlist API with functions to handle basic GET and POST requests.
 *
 *
 *     :copyright: 2019 Moodify (High-Mood)
 *     :authors:
 *            "Stan van den Broek",
 *            "Mitchell van den Bulk",
 *            "Mo Diallo",
 *            "Arthur van Eeden",
 *            "Elijah Erven",
 *            "Henok Ghebrenigus",
 *            "Jonas van der Ham",
 *            "Mounir El Kirafi",
 *            "Esmeralda Knaap",
 *            "Youri Reijne",
 *            "Siwa Sardjoemissier",
 *            "Barry de Vries",
 *            "Jelle Witsen Elias"
 */

function toggleHistory(chartName) {
    /* Onclick handles for toggle. */
    if (chartName === 'Full history') {
        $('#historySelector').text("History ");
        $('#historySelector').append("<span class=\"caret\"></span>");
        document.getElementById("headerName").innerHTML = "Full history";

        window.curData = window.histData;
        fillScrollWindow();
    } else if (chartName === 'favourites') {
        $('#historySelector').text("Favourite songs");
        $('#historySelector').append("<span class=\"caret\"></span>");

        document.getElementById("headerName").innerHTML = "Favourite Songs ";
        fillTopData();
    }
}

function fillTopData() {
    /* Request a users top ten songs and render the iframes to display them. */
    var topRequest = new XMLHttpRequest();

    topRequest.open('GET', 'http://pse-ssh.diallom.com:5000/api/tracks/topsongs/' + userid + '/10', true);
    topRequest.onload = function() {
        var allTopData = JSON.parse(this.response);
        userTopData = allTopData.resource.songs;
        window.userTopData = userTopData;

        if (topRequest.status == 200) {
            window.topData = userTopData;
            window.curData = window.topData;
            fillScrollWindow();
        }
    }
    topRequest.send();
}

function histSelect(clickEvent) {
    /** Generate similar songs based on a selected track.

    :param clickEvent: The onclick event from a selected song. **/

    song_index = clickEvent.target.id;
    displaySimilarSongs(song_index);
}

function displaySimilarSongs(song_index) {
    /** Displays the list of songs under 'More like this'.

	:param song_index: Index of the in History/Favourites list **/

    songId = window.curData[parseInt(song_index)].songid;
    window.song_index = song_index;
    adjustSlider(song_index);

    var recRequest = new XMLHttpRequest();
    recRequest.open('GET', 'http://pse-ssh.diallom.com:5000/api/tracks/recommendation/' + userid + '/' + songId + '/0.0/0.0', true);
    recRequest.onload = function() {
        var data = JSON.parse(this.response);
        var recommendations = data.resource.recommendations;
        for (var index = 0; index < 5; index++) {
            div = $('#recHist' + index);
            div.empty();
            if (recRequest.status == 200) {
                trackId = "https://open.spotify.com/embed/track/";
                trackId += recommendations[index].songid;
                content = '<iframe class="song-template" src="' + trackId + '" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>';
                div.append(content);
            } else {
                div.append("Error loading the content");
            }
        }
    }

    recRequest.send();
}

function fillScrollWindow() {
    /* Grab either 'Favourite songs' or 'History' and render iframes to
    display them. */
    data = window.curData;
    containerDiv = document.getElementById('scroll_window');
    containerDiv.innerHTML = '';

    for (var index = 0; index < data.length; index++) {
        var songdiv = document.createElement('COLUMN');
        songdiv.classList.add('songdiv');

        var songid = data[index].songid;
        songdiv.id = songid;
        songdiv.width = "100%";
        songdiv.style.backgroundColor = "black";

        var btn = document.createElement("BUTTON");
        btn.innerHTML = "Select";

        // Style is added here to ensure proper rendering.
        btn.style.margin = "0px 0px 5px 0px";
        btn.style.border = "none";
        btn.style.width = "20%";
        btn.style.height = "80px"
        btn.id = index;
        btn.onclick = function(index) {
            histSelect(index)
        };
        btn.classList.add('SongRecButton');
        btn.classList.add("btn-default");

        songdiv.appendChild(btn);

        var ifrm = document.createElement("iframe");
        ifrm.setAttribute("src", "https://open.spotify.com/embed/track/" + data[index].songid);
        ifrm.setAttribute("align", "right");
        ifrm.setAttribute("class", "song-template");
        ifrm.setAttribute("allowtransparency", "true");
        ifrm.setAttribute("allow", "encrypted-media");

        // Style is added here to ensure proper rendering.
        ifrm.style.margin = "0px 0px 5px 0px";
        ifrm.style.border = "none";
        ifrm.style.width = "80%";

        ifrm.style.height = "80px";

        songdiv.appendChild(ifrm);
        containerDiv.appendChild(songdiv);
    }
}

function adjustSlider(song_index) {
    /** Changes the mood slider positions after a song is selected
	:param song_index: Index of the song in the history/favourites list **/
    if (song_index == null) {
        excitednessSlider.slider("setValue", 50);
        happinessSlider.slider("setValue", 50);
        $('#happiness_slider_text').html(`Happiness: 50%`)
        $('#excitedness_slider_text').html(`Excitedness: 50%`)
        return;
    }

    var happiness = window.curData[song_index].happiness;
    var excitedness = window.curData[song_index].excitedness;
    var songname = document.getElementById('songdisplayname');
    songname.innerHTML = window.curData[song_index].name;

    var happiness_slider_text = $("#happiness_slider_text");
    var happiness_percentage = (happiness + 10) * 5;
    happiness_slider_text.html(`Happiness: (${Math.trunc(happiness_percentage)}%)`);

    var excitedness_slider_text = $("#excitedness_slider_text");
    var excitedness_percentage = (excitedness + 10) * 5;
    excitedness_slider_text.html(`Excitedness: (${Math.trunc(excitedness_percentage)}%)`);

    excitednessSlider.slider("setValue", Math.trunc(excitedness_percentage));
    happinessSlider.slider("setValue", Math.trunc(happiness_percentage));
};

function sendFeedback() {
    /**  Allows user to send their feedback on songs mood-analysis **/
    var happiness = document.getElementById("happiness_slider").value;
    var excitedness = document.getElementById("excitedness_slider").value;

    var uri = "http://pse-ssh.diallom.com:5000/api/tracks/mood";
    var songid = window.curData[window.song_index].songid;

    var data = {
        "songid": songid,
        "excitedness": excitedness,
        "happiness": happiness
    };

    var request = new XMLHttpRequest();
    request.open("POST", uri, true);
    request.setRequestHeader("Content-Type", 'application/json');
    request.setRequestHeader("Access-Control-Allow-Origin", 'pse-ssh.diallom.com:4000');
    request.send(JSON.stringify(data));
}

function resetFeedback() {
    /** Reset feedback sliders to their original state. **/
    var current_track = window.song_index;
    adjustSlider(current_track);
};

// Initiate sliders and set to default values.
happinessSlider.on('change', function(event) {
    $('#happiness_slider_text').html(`Happiness: ${event.value['newValue']}%`)
})

excitednessSlider.on('change', function(event) {
    $('#excitedness_slider_text').html(`Excitedness: ${event.value['newValue']}%`)
})

// Show history data when websites is opened.
var request = new XMLHttpRequest();
request.open('GET', 'http://pse-ssh.diallom.com:5000/api/tracks/history/' + userid + '/20', true);
request.onload = function() {
    var allData = JSON.parse(this.response);
    userData = allData.resource.songs;
    window.histData = userData;
    window.curData = window.histData;

    if (request.status == 200) {
        fillScrollWindow();
    }
}
request.send();

// Initialize feedback sliders.
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
