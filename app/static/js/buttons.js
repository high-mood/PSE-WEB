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
    colours = ['rgba(255, 153, 0, 1)', 'rgba(0, 255, 255, 1)', 'rgba(64, 255, 0, 1)', 'rgba(0, 64, 255, 1)', 'rgba(191, 0, 255, 1)', 'rgba(255, 0, 64, 1)', 'rgba(255, 255, 0, 1)', 'rgba(128, 0, 255, 1)', 'rgba(0, 255, 0, 1)'];
    for (let i = 0; i < metrics.length; i++) {
        spawnButton(metrics[i], id);
        document.getElementById(metrics[i]).setAttribute("style", "background-color:" + colours[i]);
        console.log(colours[i]);
    }
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