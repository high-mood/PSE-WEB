$('#heatmapRow').hide();

var userid = $('#username').html()
var request = new XMLHttpRequest();
var created = 'False'; // todo this seems not to be used, remove if not needed?

// Send request for the data needed in the mood charts.
request.open('GET', 'http://pse-ssh.diallom.com:5000/api/tracks/history/' + userid + '/0', true)
request.onload = function() {
    var alldata = JSON.parse(this.response)
    userdata = alldata.resource
    window.userdata = userdata
    if ((request.status >= 200 && request.status < 400) || request.status == 0) {
        // RadarChart is made first as it is shown first
        createRadarChart(userdata);
        giveText(userdata, "radarText");
        document.getElementsByClassName("radar")[0].onmousemove = hoverRadar;
        document.getElementsByClassName("radar")[0].onmouseout = resetRadarText;
    }
}
request.send()

// Function to toggle the chart that is shown.
function toggleMoodCharts(chartname) {
    if (chartname === 'radarChart') {
        $('#moodChartSelector').text("Radar Chart ")
        $('#moodChartSelector').append("<span class=\"caret\"></span>")
        $('#radarChartRow').show();
        $('#heatmapRow').hide();
    }
    else if (chartname === 'heatmap') {
        $('#moodChartSelector').text("Heatmap ")
        $('#moodChartSelector').append("<span class=\"caret\"></span>")
        // The heatmap may not have been rendered yet so it is generated here.
        if ($('#heatmap').children().length == 0) {
            title = ""
            createHeatmap("heatmap", title, -10, 10, 50, "excitedness", -10, 10, 50, "happiness", userdata);
            giveText(userdata, "heatmapText");
        }
        $('#radarChartRow').hide();
        $('#heatmapRow').show();
    }
}
