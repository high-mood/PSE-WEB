var mean_excitedness, mean_happiness;
const graphTexts = ["\
High Excitedness, High Happiness <br> (happy, upbeat, energetic)<br><br>\
The music you listen to is generally very happy and has high energy. <br><br>\
This means that the beat is faster, a higher bpm (beats per minute), <br> \
and that the feeling described when people listen to these songs are in the line of happy, cheerful, amazed. <br><br>\
You seem to be a very cheerful and upbeat person.",
"\
High Excitedness, Low Happiness <br> (upbeat, pumped, empowering, angry)<br><br>\
The music you listen to is generally less happy but has high energy.<br><br>\
This means that the beat might be faster, a higher bpm (beats per minute),<br>\
or the songs have a more empowering feeling to them.<br><br>\
The feeling described when people listen to these songs are in the line of empowering, angry, upbeat, pumped.<br><br>\
You seem like someone that loves to feel empowered by music, or perhaps a little frustrated",
"\
Low Excitedness, High Happiness <br>(nostalgic, peaceful)<br><br>\
The music you listen to is generally happy but has less energy.<br><br>\
This means that the beat is a bit slower, lower bpm (beats per minute),<br>\
and that the music is pretty relaxed, but has a generally happy vibe to it.<br><br>\
You seem like a very relaxed and mellow person.",
"\
Low Excitedness, Low Happiness<br>(sad, angry songs)<br><br>\
The music you listen to is generally slow and has less energy.<br><br>\
This means that the beat is pretty slow, low bpm (beats per minute),<br>\
and that the music is perceived as sad.<br><br>\
You seem sad or a bit down on your luck."];

const heatMapText = "In this heatmap the happines and excitement values<br>\
are displayed on the x and y axis.<br>\
The intensity of the color is determined by the density of songs.<br><br>\
The more songs are in that area the brighter red that spot will be.";

/** Gives a div corresponding to a given id description of the user's mood.*/
function giveText(data, id) {
    var texts = graphTexts;

    mean_excitedness = data.mean_excitedness;
    mean_happiness = data.mean_happiness;

   if (id == "heatmapText") {
        $(`#${id}`).html(heatMapText);
   } else {
        $(`#${id}`).html(getText(mean_excitedness, mean_happiness, texts));
   }
}

/* After mouse out the text in the radarText div is reset. */
function resetRadarText() {
    $("#radarText").html(getText(mean_excitedness, mean_happiness, graphTexts));
}

/** Hovering over a graphs quadrants changes the text.
 * DISCLAIMER: Only works for graphs that have a centered (0, 0).
 */
function hoverRadar(e) {
    var xy_pos = getXYpos(this);
    x = e.pageX;
    y = e.pageY;

    if (this.tagName === "svg") {
        x = x - xy_pos['xp'] - this.width.baseVal.value/2;
        y = this.height.baseVal.value/2 - (y - xy_pos['yp']);
    } else {
        x = x - xy_pos['xp'] - this.offsetWidth/2;
        y = this.offsetHeight/2 - (y - xy_pos['yp']);
    }

    $('#radarText').html(getText(y, x, graphTexts));
}

/** Gets the position of the mouse within a specific div.*/
function getXYpos(elem) {
    var x = 0;
    var y = 0;

    if (elem.tagName === "svg") {
        elem = elem.parentElement;    // set elem to its offsetParent
    } else {
        x = elem.offsetLeft;
        y = elem.offsetTop;

        elem = elem.offsetParent;    // set elem to its offsetParent
    }

    //use while loop to check if elem is null
    // if not then add current elem’s offsetLeft to x
    //offsetTop to y and set elem to its offsetParent
    while(elem != null) {
      x = parseInt(x) + parseInt(elem.offsetLeft);
      y = parseInt(y) + parseInt(elem.offsetTop);
      elem = elem.offsetParent;
    }

    // returns an object with "xp" (Left), "=yp" (Top) position
    return {'xp':x, 'yp':y};
  }

/** Gets the corresponding text corresponding to which quadrant you hover over. */
function getText(m_excitedness, m_happiness, texts) {
    if (m_excitedness >= 0) {
        if (m_happiness >= 0) {
            return texts[0];
        } else {
            return texts[1];
        }
    } else {
        if (m_happiness >= 0) {
            return texts[2];
        } else {
            return texts[3];
        }
    }
}