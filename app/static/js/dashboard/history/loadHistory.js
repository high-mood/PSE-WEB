$('#favRo').hide();
// TODO remove hardcode
var userid = 'snipy12';

var request = new XMLHttpRequest();

request.open('GET', 'http://localhost:5000/api/tracks/history/' + userid + '/0', true)
request.onload = function() {
    var alldata = JSON.parse(this.response);
    userdata = alldata.resource;
    window.userdata = userdata;
    if (request.status >= 200 && request.status < 400) {
        // Song history
        createHistory(userdata);
    }
}
request.send();

function toggleHistory(chartname) {
    if (chartname === 'history') {
        $('#historySelector').text("History ");
        $('#historySelector').append("<span class=\"caret\"></span>");
        $('#historyRow').show();
        $('#favRow').hide();
    }
    else if (chartname === 'favourites') {
        $('#historySelector').text("Favourites ");
        $('#historySelector').append("<span class=\"caret\"></span>");
        topdata = getTopData();
        if ($('favRow').children().length == 0) {
            // Favourites.
            createTop(topdata);
        }
        $('#historyRow').hide();
        $('#favRow').show();
    }
}

function getTopData() {
    var topRequest = new XMLHttpRequest();

    topRequest.open('GET', 'http://localhost:5000/api/tracks/topsongs/' + userid + '/5', true, {
        headers: {
            'Access-Control-Allow-Origin': 'pse-ssh.diallom.com'
        }
    })
    topRequest.onload = function() {
        var allTopData = JSON.parse(this.response);
        userTopData = allTopData.resource;
        if (topRequest.status >= 200 && topRequest.status < 400) {
            return userTopData;
        } else {
            document.getElementById("userwelcome").innerHTML = "Error retrieving data!";
        }
    }
    topRequest.send();
}

