function generateButtons(id) {
    metrics = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence'];
    colours = ['#ff8a80', '#ea80fc', '#8c9eff', '#80d8ff', '#a7ffeb', '#ccff90', '#ffff8d', '#ffd180', '#ff9e80'];
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

function startStates(metrics, on) {
    metrics.forEach(element => {
        elem = document.getElementById(element);

        if (on.includes(element)) {
            elem.style.opacity = 1;
            showLine(id);
        } else {
            elem.style.opacity = 0.5;
            hideLine(id);    
        }
    });
}