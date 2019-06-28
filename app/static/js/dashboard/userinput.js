/* userinput.js
 *
 * This file defines JQuery UI slider objects used in the section 'Analytics'.
 *
 *     This file contains the structure of the playlist API with functions to handle basic GET and POST requests.
 *
 *
 *     :copyright: 2019 Moodify (High-Mood)
 *     :authors:
 *            "Stan van den Broek",
 *            "Mitchell van den Bulk",
 *            "Mo Diallo",
 *            "Arthur van Eeden",
 *            "Elijah Erven",
 *            "Henok Ghebrenigus",
 *            "Jonas van der Ham",
 *            "Mounir El Kirafi",
 *            "Esmeralda Knaap",
 *            "Youri Reijne",
 *            "Siwa Sardjoemissier",
 *            "Barry de Vries",
 *            "Jelle Witsen Elias"
 */
var timeframeSliderObj = $("#timeframe-slider").slider({
    id: "timeframe-slider",
    orientation: 'horizontal',
    min: 1,
    max: 24,
    range: true,
    value: [8, 16]
});

var daysSliderObj = $("#days-slider").slider({
    id: "days-slider",
    orientation: 'horizontal',
    min: 2,
    max: 50,
    value: 10
});

var songsSliderObj = $("#songs-slider").slider({
    id: "songs-slider",
    orientation: 'horizontal',
    min: 2,
    max: 200,
    value: 10
});

$("#timeframe-slider-div").toggle()
$("#songs-slider-div").toggle()

var happinessSlider = $("#happiness_slider").slider({
    id: "happiness_slider",
    orientation: 'horizontal',
    min: 0,
    max: 100,
    range: false,
    value: 50,
    animate: "fast"
});

var excitednessSlider = $("#excitedness_slider").slider({
    id: "excitedness_slider",
    orientation: 'horizontal',
    min: 0,
    max: 100,
    range: false,
    value: 50,
    animate: "fast"
});
