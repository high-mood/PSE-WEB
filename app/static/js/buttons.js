var metrics = [];

function add_metrics(id) {
    metrics.push(document.getElementById(id).textContent);
    return parse_metrics(id);
}

function remove_metrics(id) {
    metrics.filter(function(ele){
        return ele != value;
    });
    return parse_metrics(id);
}

function parse_metrics(id) {
    var metricstring = "";
    metrics.forEach(element => {
        metricstring += element;
    });

    return metricstring;
}

function generateButtons(id) {
    metrics = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence'];
    colours = ['rgb(255, 153, 0)', 'rgb(0, 255, 255)', 'rgb(64, 255, 0)', 'rgb(0, 64, 255)', 'rgb(191, 0, 255)', 'rgb(255, 0, 64)', 'rgb(255, 255, 0)', 'rgb(128, 0, 255)', 'rgb(255, 0, 255)'];
    for (let i = 0; i < metrics.length; i++) {
        spawnButton(metrics[i], id);
        document.getElementById(metrics[i]).setAttribute("style", "background-color:" + colours[i]);
    }
}

function spawnButton(metric, id) {
    buttonsDiv = document.getElementById(id);

    buttonDiv = document.createElement("div");
    buttonDiv.setAttribute("id", metric);
    buttonDiv.setAttribute("class", "linechartMetricButton");
    buttonDiv.setAttribute("style", "float: left; margin: 3px;");
    buttonDiv.setAttribute("onclick", "press(this.id)");
    buttonDiv.innerHTML = metric;
    buttonsDiv.appendChild(buttonDiv);
}

function press(id) {
    elem = document.getElementById(id);
    if (elem.style.opacity == 0.5) {
        elem.style.opacity = 1;
        showLine(id);
    } else {
        elem.style.opacity = 0.5;
        hideLine(id);
    }
}