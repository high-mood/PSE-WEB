/** userinput.js
 *
 * This file defines JQuery UI slider objects used in the section 'Analytics'.

 *     @copyright: 2019 Moodify (High-Mood)
 *     @author "Stan van den Broek",
 *     @author "Mitchell van den Bulk",
 *     @author "Mo Diallo",
 *     @author "Arthur van Eeden",
 *     @author "Elijah Erven",
 *     @author "Henok Ghebrenigus",
 *     @author "Jonas van der Ham",
 *     @author "Mounir El Kirafi",
 *     @author "Esmeralda Knaap",
 *     @author "Youri Reijne",
 *     @author "Siwa Sardjoemissier",
 *     @author "Barry de Vries",
 *     @author "Jelle Witsen Elias"
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
