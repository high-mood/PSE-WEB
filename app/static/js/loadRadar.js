

function createRadarChart(userdata) {

  /* Radar chart design created by Nadieh Bremer - VisualCinnamon.com */
  var margin = {top: 100, right: 100, bottom: 100, left: 100},
    width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
    height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);


  var color = d3.scaleOrdinal().range(["#EDC951","#EDC951"])

  var radarChartOptions = {
    // w: width,
    // h: height,
    w: 500,
    h: 500,
    margin: margin,
    maxValue: 10,
    levels: 5,
    opacityArea: 0.1,
    roundStrokes: true,
    color: color
  };

  document.title = userdata.userid + "\'s  Mood";

  var finaldata = [];
  var song;
  for (i = 0; i < userdata.songs.length; i++) {

    song = {
      name : 'Song',
      axes : [
        {axis:"High Excitedness",value:userdata.songs[i].excitedness},
        {axis:"High Happiness",value:userdata.songs[i].happiness},
        {axis:"Low Excitedness",value:0.0},
        {axis:"Low Happiness",value:0.0}
      ]
    }
    finaldata.push(song);
  }

  let svg_radar1 = RadarChart(".radarChart", finaldata, radarChartOptions);
}

function changeActiveTab(el) {

  var tabs = document.getElementsByClassName('active');

  if (tabs.length > 0) {
    tabs[0].classList.remove('active');
  }

  var newTab = document.getElementById(el);
  newTab.classList.add('active');

}

function showTabs() {

    var x = document.getElementById("myNavigationBar");

    if (x.className === "navigation-bar") {
        x.className += " responsive";
    } else {
        x.className = "navigation-bar";
    }
}

function navigateTo(location) {

  var elmnt = document.getElementById(location);
  elmnt.scrollIntoView({behavior: 'smooth'});

  // changeActiveTab(location + 'Tab');
  showTabs();

}

document.addEventListener("DOMContentLoaded", function() {

  tabHighLightFromPosition()

});

window.addEventListener("scroll", function() {

  tabHighLightFromPosition();

})

function tabHighLightFromPosition() {

  var pageLocations = [];
  var pages = document.getElementsByClassName('mainPage');

  for (var i = 0; i < pages.length; i++) {
    var border = pages[i].getBoundingClientRect();
    pageLocations.push(border.top * border.top)
  }

  var min = Math.min.apply(null, pageLocations);
  var closestTab = pageLocations.indexOf(min);

  // changeActiveTab(pages[closestTab].id + 'Tab');

  var x = document.getElementById("myNavigationBar");

  if (x.className === "navigation-bar responsive") {
      x.className = "navigation-bar";
  }

}
