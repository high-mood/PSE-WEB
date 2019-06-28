// toggles specific line (for button clicks)
function toggleLine(buttonId) {
    button = $(`#${buttonId}`);
    if (button.css('opacity') == '1') {
        button.css('opacity', '0.3');
        hideLine(buttonId);
    }
    else {
        button.css('opacity', '1');
        showLine(buttonId);
    }
}

// toggles all buttons
function toggleAll() {
    var lineNames = ["excitedness", "happiness", "acousticness", "danceability", 
    "energy", "instrumentalness", "liveness", "speechiness", 
    "tempo", "valence"];

    // check if all buttons toggled
    var allToggled = true;
    for (var i in lineNames) {
        if (d3.select("#" + lineNames[i] + "line").style("visibility") == "hidden") {
            allToggled = false;
            break;
        }
    }
    if (allToggled) {
        for (var i in lineNames) {
            toggleLine(lineNames[i]);
        }
    }
    else {
        for (var i in lineNames) {
            if (d3.select("#" + lineNames[i] + "line").style("visibility") == "hidden") {
                toggleLine(lineNames[i]);
            }
        }
    }
}

// hides a given line, shows and hides relevant axes
function hideLine(name) {

    d3.selectAll("#" + name + "line")
        .style("visibility", "hidden");
    d3.selectAll("." + name + "daysdot")
        .style("visibility", "hidden");
    d3.selectAll("." + name + "songdot")
        .style("visibility", "hidden");


    // show correct right y axis
    if (name == "tempo") {
        d3.selectAll(".tempo.axis")
            .style("visibility", "hidden");

        if (d3.select("#excitednessline").style("visibility") == "visible" ||
            d3.select("#happinessline").style("visibility") == "visible") {
            d3.selectAll(".moods.axis").style("visibility", "visible");
        }
    }
    else if (name == "happiness") {
        if (d3.select("#excitednessline").style("visibility") == "hidden") {
            d3.selectAll(".moods.axis").style("visibility", "hidden");
            if (d3.select("#tempoline").style("visibility") == "visible") {
                d3.selectAll(".tempo.axis").style("visibility", "visible");
            }           
        }
    }
    else if (name == "excitedness") {
        if (d3.select("#happinessline").style("visibility") == "hidden") {
            d3.selectAll(".moods.axis").style("visibility", "hidden");
            if (d3.select("#tempoline").style("visibility") == "visible") {
                d3.selectAll(".tempo.axis").style("visibility", "visible");
            }           
        }
    }
}

// shows a given line and proper axes
function showLine(name) {
    d3.selectAll("#" + name + "line")
        .style("visibility", "visible");
    d3.selectAll("." + name + "daysdot")
        .style("visibility", "visible");
    d3.selectAll("." + name + "songdot")
        .style("visibility", "visible");

    // show correct right y axis
    if (name == "tempo") {
        d3.selectAll(".tempo.axis")
            .style("visibility", "visible");
        d3.selectAll(".moods.axis")
            .style("visibility", "hidden");
    }
    if (name == "happiness" || name == "excitedness") {
        d3.selectAll(".moods.axis")
            .style("visibility", "visible");
        d3.selectAll(".tempo.axis")
            .style("visibility", "hidden");
    }
}