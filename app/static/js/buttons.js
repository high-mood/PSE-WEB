metrics = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence'];
colours = ['#ff8a80', '#ea80fc', '#8c9eff', '#80d8ff', '#a7ffeb', '#ccff90', '#ffff8d', '#ffd180', '#ff9e80'];

/** 
 * Generates a button for each metric given in the array.
 * Gives each button the corresponding color.
 */
function generateButtons(id) {

    for (let i = 0; i < metrics.length; i++) {
        spawnButton(metrics[i], id);
        document.getElementById(metrics[i]).setAttribute("style", "background-color:" + colours[i]);
    }
}

/**
 * Creates one button element on the webpage, in the div for all buttons. 
*/ 
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

/** Onclick event:
 * The opacity of the button clicked changes accordingly to if it
 * is pressed or not.
 * If it was pressed to "on"-state the line in the graph is shown,
 * otherwise it is hidden
 */
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

/** startStates(metrics, on)
 * @param {array(string)}   on  A list of metrics of which the buttons have to be on.
 * 
 * Given the list of metrics those specific buttons are "pressed",
 * these buttons are shown in the "on"-state.
*/
function startStates(on) {
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