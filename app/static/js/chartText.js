const radarTexts = ["<br><br><br><br><br><br><br><br>\
High Excitedness, High Happiness <br> (happy, upbeat, energetic)<br><br>\
The music you listen to is generally very happy and has high energy. <br><br>\
This means that the beat is faster, a higher bpm (beats per minute), <br> \
and that the feeling described when people listen to these songs are in the line of happy, cheerful, amazed. <br><br>\
You seem to be a very cheerful and upbeat person.",
"<br><br><br><br><br><br><br><br>High Excitedness, Low Happiness <br> (upbeat, pumped, empowering, angry)<br><br>\
The music you listen to is generally less happy but has high energy.<br><br>\
This means that the beat might be faster, a higher bpm (beats per minute),\
or the songs have a more empowering feeling to them.<br><br>\
The feeling described when people listen to these songs are in the line of empowering, angry, upbeat, pumped.<br><br>\
You seem like someone that loves to feel empowered by music, or perhaps a little frustrated",
"<br><br><br><br><br><br><br><br>Low Excitedness, High Happiness (nostalgic, peaceful)<br><br>\
The music you listen to is generally happy but has less energy.<br><br>\
This means that the beat is a bit slower, lower bpm (beats per minute),<br>\
and that the music is pretty relaxed, but has a generally happy vibe to it.<br><br>\
You seem like a very relaxed and mellow person.",
"<br><br><br><br><br><br><br><br>Low Excitedness, Low Happiness<br>(sad, angry songs)<br><br>\
The music you listen to is generally slow and has less energy.<br><br>\
This means that the beat is pretty slow, low bpm (beats per minute), and that the music is perceived as sad.<br><br>\
You seem sad or a bit down on your luck."];

function giveText(data, id) {
    var texts;
    if (id == "radarText") {
        texts = radarTexts;
    }

    document.getElementById(id).innerHTML = getText(data.mean_excitedness, data.mean_happiness,texts);
}

function resetRadarText(data) {
    giveText(data, "radarText");
}

function hoverRadar(e) {
    var xy_pos = getXYpos(this);
    x = e.pageX;
    y = e.pageY;

    x = x - xy_pos['xp'] - this.offsetWidth/2;
    y = this.offsetHeight/2 - (y - xy_pos['yp']);
    document.getElementById('radarText').innerHTML = getText(y, x, radarTexts);
}

function getXYpos(elm) {
    x = elm.offsetLeft;        // set x to elm’s offsetLeft
    y = elm.offsetTop;         // set y to elm’s offsetTop
  
    elm = elm.offsetParent;    // set elm to its offsetParent
  
    //use while loop to check if elm is null
    // if not then add current elm’s offsetLeft to x
    //offsetTop to y and set elm to its offsetParent
    while(elm != null) {
      x = parseInt(x) + parseInt(elm.offsetLeft);
      y = parseInt(y) + parseInt(elm.offsetTop);
      elm = elm.offsetParent;
    }
  
    // returns an object with "xp" (Left), "=yp" (Top) position
    return {'xp':x, 'yp':y};
  }

function getText(mean_excitedness, mean_happiness, texts) {
    if (mean_excitedness >= 0) {
        if (mean_happiness >= 0) {
            return texts[0];
        } else {
            return texts[1];
        }
    } else {
        if (mean_happiness >= 0) {
            return texts[2];
        } else {
            return texts[3];
        }
    }
}