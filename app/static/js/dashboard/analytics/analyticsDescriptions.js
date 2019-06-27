function analyticsDescription(chartName) {
    var description = $("#analyticsDescription");

    description.empty();

    if (chartName == "songs") {
        description.html(songText)
    }
    else if (chartName == "days") {
        description.html(daysText)
    }
    else if (chartName == "bar") {
        description.html(barText)
    }
}

var daysText = "The graph currently displays average statistics of the past days on which you have listened to music on Spotify.\
By hovering over the datapoints you can see the exact values for a given day.\
You can click one of the buttons below to show or hide the corresponding parameter in the graph.\
The slider above the graph allows you to select the timeframe of the graph."

var songText = "The graph currently displays average statistics of the past songs you have listened to on Spotify.\
By hovering over the datapoints you can see the exact values for a given song.\
You can click one of the buttons below to show or hide the corresponding parameter in the graph.\
The slider above the graph allows you to select the number of displayed songs."

var barText = "The graph currently displays average excitedness (blue) and happiness (green) per hour in a day.\
The displayed excitedness and happiness are averages over all the tracks you have listened to since you have started using Moodify.\
The slider above the graph allows you to select the time frame for which you can see your average excitedness and happiness."
