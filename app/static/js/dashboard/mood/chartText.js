var mean_excitedness, mean_happiness;
const graphTexts = ["\
<b>Excited:</b> <br><br>\
<i>\"Choose thoughts that give you the emotions of being alive and excited about life.\"</i> <br>\
― Bryant McGill, Simple Reminders: Inspiration for Living Your Best Life <br><br>\
Like this quote you choose to listen to music that makes you feel alive and excited about life. <br><br>\
When you're excited you have a heightened state of energy, enthusiasm and eagerness, <br>\
this means that the songs you listen to contain a high excitedness and happiness. <br>\
They are happy, upbeat and energetic, the beat is faster and the song has a higher bpm (beats per minute). <br><br>\
People generally describe this kind of music as happy, cheerful and amazed. <br>\
You seem to be a very cheerful and upbeat person.",
"\
<b>Angry:</b> <br><br>\
<i>\"Anybody can become angry - that is easy, but to be angry with the right person <br>\
and to the right degree and at the right time and for the right purpose, <br>\
and in the right way - that is not within everybody's power and is not easy.\"</i> <br>\
 ― Aristotle <br><br>\
Like this quote you choose to become angry to the right degree, at the right time and\
for the right purpose. You choose to listen to music to control your anger. <br><br>\
When you're angry you show a strong feeling of displeasure, opposition or hostility, <br>\
this means that the songs you listen to contain a high excitedness and low happiness. <br>\
They are upbeat, pumped, empowering and angry, the beat might be faster and the song has a higher bpm (beats per minute). <br><br>\
People generally describe this kind of music as empowering, angry, upbeat and pumped. <br>\
You seem like someone that loves to feel empowered by music, or perhaps you're a little frustrated.",
"\
<b>Mellow:</b> <br><br>\
<i>\"You know, I'm a pretty mellow guy. I'm pretty easy-going. I see everyone's perspective.\"</i> <br>\
― Paul Walker <br><br>\
Like this quote you're a person who likes to listen to easy-going music. <br><br>\
When you're mellow you are pleasant, agreeable and laid-back, <br>\
this means that the songs you listen to contain a low excitedness and high happiness. <br>\
They are nostalgic and peaceful, the beat is a bit slower and the song has a low bpm (beats per minute). <br><br>\
People generally describe this kind of music as pretty relaxed but with a happy vibe. <br>\
You seem like a very relaxed and mellow person.",
"\
<b>Sad:</b> <br><br>\
<i>\"There is a sacredness in tears. They are not the mark of weakness, but of power. <br>\
They speak more eloquently than ten thousand tongues. They are the messengers of <br>\
overwhelming grief, of deep contrition, and of unspeakable love.\"</i> <br>\
― Washington Irving <br><br>\
Like this quote you show power in your sadness. You show your overwhelming grief, <br>\
deep contrition and unspeakable love in the music that you listen to. <br><br>\
When you're sad you express grief or unhappiness, <br>\
this means that the songs you listen to contain a low excitedness and low happiness. <br>\
They are sad and angry, the beat is pretty slow and the song has a low bpm (beats per minute). <br><br>\
People generally perceive this kind of music as sad. <br>\
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
