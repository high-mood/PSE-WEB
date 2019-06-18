const radarTexts = ["<br><br><br><br><br><br><br><br><br>\
High Excitedness, High Happiness <br> (happy, upbeat, energetic)<br><br>\
The music you listen to is generally very happy and has high energy. <br><br>\
This means that the beat is faster, a higher bpm (beats per minute), <br> \
and that the feeling described when people listen to these songs are in the line of happy, cheerful, amazed. <br><br>\
You seem to be a very cheerful and upbeat person.",
"<br><br><br><br><br><br><br><br><br>High Excitedness, Low Happiness <br> (upbeat, pumped, empowering, angry)<br><br>\
The music you listen to is generally less happy but has high energy.<br><br>\
This means that the beat might be faster, a higher bpm (beats per minute),\
or the songs have a more empowering feeling to them.<br><br>\
The feeling described when people listen to these songs are in the line of empowering, angry, upbeat, pumped.<br><br>\
You seem like someone that loves to feel empowered by music, or perhaps a little frustrated",
"<br><br><br><br><br><br><br><br><br>Low Excitedness, High Happiness (nostalgic, peaceful)<br><br>\
The music you listen to is generally happy but has less energy.<br><br>\
This means that the beat is a bit slower, lower bpm (beats per minute),<br>\
and that the music is pretty relaxed, but has a generally happy vibe to it.<br><br>\
You seem like a very relaxed and mellow person.",
"<br><br><br><br><br><br><br><br><br>Low Excitedness, Low Happiness<br>(sad, angry songs)<br><br>\
The music you listen to is generally slow and has less energy.<br><br>\
This means that the beat is pretty slow, low bpm (beats per minute), and that the music is perceived as sad.<br><br>\
You seem sad or a bit down on your luck."];

function giveText(data, id) {
    var text;
    if (id == "radarText") {
        text = radarText(data);
    }

    document.getElementById(id).innerHTML = text;
}

function radarText(data) {
    if (data.mean_excitedness > 0) {
        if (data.mean_happiness > 0) {
            return radarTexts[0];
        } else {
            return radarTexts[1];
        }
    } else {
        if (data.mean_happiness > 0) {
            return radarTexts[2];
        } else {
            return radarTexts[3];
        }
    }
}