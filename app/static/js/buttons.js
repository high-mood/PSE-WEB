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
    // colours = [rgba(255, 153, 0, 1), ];
    metrics.forEach(element => {
        spawnButton(element, id);
    });
}

function spawnButton(metric, id) {
    buttonsDiv = document.getElementById(id);

    buttonDiv = document.createElement("div");
    buttonDiv.setAttribute("id", metric);
    buttonDiv.setAttribute("class", "linechartMetricButton");
    buttonDiv.setAttribute("style", "float: left; margin: 3px;");
    buttonDiv.innerHTML = metric;
    // buttonDiv.setAttribute("onclick", )
    buttonsDiv.appendChild(buttonDiv);
}