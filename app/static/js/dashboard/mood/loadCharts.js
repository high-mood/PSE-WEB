$('#heatmapRow').hide();
// var userid = 'snipy12';
var userid = $('#username').html()
var request = new XMLHttpRequest();
var created = 'False';

// request.open('GET', 'https://cors-anywhere.herokuapp.com/http://randomelements.nl/highmood/data/dummydata.json', true)
request.open('GET', 'http://localhost:5000/api/tracks/history/' + userid + '/0', true)
request.onload = function() {
    var alldata = JSON.parse(this.response)
    userdata = alldata.resource
    window.userdata = userdata
    if ((request.status >= 200 && request.status < 400) || request.status == 0) {
        // RadarChart
        createRadarChart(userdata);
        giveText(userdata, "radarText");

        document.getElementsByClassName("radar")[0].onmousemove = hoverRadar;
        document.getElementsByClassName("radar")[0].onmouseout = resetRadarText;
    }
}
request.send()

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
        if ($('#heatmap').children().length == 0) {
            // Heatmap
            title = ""
            // title = "A heatmap of the excitedness and happiness of your songs."
            createHeatmap("heatmap", title, -10, 10, 50, "excitedness", -10, 10, 50, "happiness", userdata);
            giveText(userdata, "heatmapText");
        }
        $('#radarChartRow').hide();
        $('#heatmapRow').show();
    }
}
