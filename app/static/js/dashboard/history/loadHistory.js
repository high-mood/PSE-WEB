/** loadHistory.js
 *
 * This file contains javascript code to properly render the 'Review' section.
 *
 * To do so, it defines JQuery UI slider objects used in the section 'Analytics'.
 * It contains the structure of the playlist API with functions to handle basic GET and POST requests.
 *
 *
 *     @copyright 2019 Moodify (High-Mood)
 *     @author "Stan van den Broek",
 *     @author "Mitchell van den Bulk",
 *     @author "Mo Diallo",
 *     @author "Arthur van Eeden",
 *     @author "Elijah Erven",
 *     @author "Henok Ghebrenigus",
 *     @author "Jonas van der Ham",
 *     @author "Mounir El Kirafi",
 *     @author "Esmeralda Knaap",
 *     @author "Youri Reijne",
 *     @author "Siwa Sardjoemissier",
 *     @author "Barry de Vries",
 *     @author "Jelle Witsen Elias"
 */

/** @description         Onclick handler for toggling between modes..
 *
 *  @param chartName     Name of currently selected mode.
 */
function toggleHistory(chartName) {
    if (chartName === 'history') {
        $('#historySelector').text("History ");
        $('#historySelector').append("<span class=\"caret\"></span>");
        document.getElementById("headerName").innerHTML = "History";

        window.curData = window.histData;
        fillScrollWindow();
    } else if (chartName === 'favourites') {
        $('#historySelector').text("Favourite songs");
        $('#historySelector').append("<span class=\"caret\"></span>");

        document.getElementById("headerName").innerHTML = "Favourite Songs ";
        fillTopData();
    }
}

/** @description    Request a users top ten songs and render the iframes to
 *                  display them.
 */
function fillTopData() {
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

/** @description        Generate similar songs based on a selected track.
 *
 *  @param clickEvent   The onclick event from a selected song.
 */
function histSelect(clickEvent) {

    song_index = clickEvent.target.id;
    displaySimilarSongs(song_index);
}

/** @description        Displays the list of songs under 'More like this'.
 *
 * @param song_index    Index of the in History/Favourites list
 */
function displaySimilarSongs(song_index) {

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

/** @description    Grab either 'Favourite songs' or 'History' and render
  *                 iframes to display them.
  */
function fillScrollWindow() {
    data = window.curData;
    containerDiv = document.getElementById('scroll_window');
    containerDiv.innerHTML = '';

    // Loop to the amount of songs returned for current user
    for (var index = 0; index < data.length; index++) {

        // Create main div for song and set style
        var songdiv = document.createElement('COLUMN');
        var songid = data[index].songid;
        songdiv.classList.add('songdiv');
        songdiv.id = songid;
        songdiv.width = "100%";
        songdiv.style.backgroundColor = "black";

        // Create select button for song and set style
        var btn = document.createElement("BUTTON");
        btn.innerHTML = "Select";
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

        // Create Spotify play widget for song
        var ifrm = document.createElement("iframe");
        ifrm.setAttribute("src", "https://open.spotify.com/embed/track/" + data[index].songid);
        ifrm.setAttribute("align", "right");
        ifrm.setAttribute("class", "song-template");
        ifrm.setAttribute("allowtransparency", "true");
        ifrm.setAttribute("allow", "encrypted-media");

        // Spotify widget style is added here to ensure proper rendering.
        ifrm.style.margin = "0px 0px 5px 0px";
        ifrm.style.border = "none";
        ifrm.style.width = "80%";
        ifrm.style.height = "80px";

        // Append widget and select button to songdiv, append songdiv to container
        songdiv.appendChild(btn);
        songdiv.appendChild(ifrm);
        containerDiv.appendChild(songdiv);
    }
}

/** @description        Changes the mood slider positions after a song is
  *                     selected
  *
  * @param song_index   Index of the song in the history/favourites list
  */
function adjustSlider(song_index) {
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

    // Set happiness slider to song happiness
    var happiness_slider_text = $("#happiness_slider_text");
    var happiness_percentage = (happiness + 10) * 5;
    happiness_slider_text.html(`Happiness: (${Math.trunc(happiness_percentage)}%)`);

    // Set exitedness slider to song exitedness
    var excitedness_slider_text = $("#excitedness_slider_text");
    var excitedness_percentage = (excitedness + 10) * 5;
    excitedness_slider_text.html(`Excitedness: (${Math.trunc(excitedness_percentage)}%)`);

    excitednessSlider.slider("setValue", Math.trunc(excitedness_percentage));
    happinessSlider.slider("setValue", Math.trunc(happiness_percentage));
};

/**  @description   Allows user to send their feedback on songs mood-analysis
**/
function sendFeedback() {
    var uri = "http://pse-ssh.diallom.com:5000/api/tracks/mood";
    var songid = window.curData[window.song_index].songid;

    var data = {
        "songid": songid,
        "excitedness": excitednessSlider.slider("getValue"),
        "happiness": happinessSlider.slider("getValue")
    };

    var request = new XMLHttpRequest();
    request.open("POST", uri, true);
    request.setRequestHeader("Content-Type", 'application/json');
    request.setRequestHeader("Access-Control-Allow-Origin", 'pse-ssh.diallom.com:4000');
    request.send(JSON.stringify(data));
}

/** @description    Reset feedback sliders to their original state. **/
function resetFeedback() {
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
