function createMainPageChart(mainPageDiv,chartId,chartClass,textId,textClass,even,bigScreen) {

  mainDiv = document.getElementById(mainPageDiv);

  chartDiv = document.createElement("div");
  chartDiv.setAttribute("id",chartId);
  textDiv = document.createElement("div");
  textDiv.setAttribute("id",textId);

  if (bigScreen) {
    mainDiv.setAttribute("class","mainPage");
    chartDiv.setAttribute("class","innerChartDiv " + chartClass);
    textDiv.setAttribute("class","innerTextDiv " + textClass);
    if (even) { // even number of mainpage elements before
      mainDiv.appendChild(chartDiv);
      mainDiv.appendChild(textDiv);
    } else { // odd number of mainpage elements before
      mainDiv.appendChild(textDiv);
      mainDiv.appendChild(chartDiv);
    }
  } else { // small screen (smartphone)
    mainDiv.setAttribute("class","mainPageSmall");
    chartDiv.setAttribute("class","innerChartDivSmall " + chartClass);
    textDiv.setAttribute("class","innerTextDivSmall " + textClass);
    mainDiv.appendChild(chartDiv);
    mainDiv.appendChild(textDiv);
  }
}

function createMainPageTopChart(mainPageDiv,topSongsId,topSongsClass,chartId,chartClass,textId,textClass,bigScreen) {

  mainDiv = document.getElementById(mainPageDiv);

  topSongsDiv = document.createElement("div");
  topSongsDiv.setAttribute("id",topSongsId);
  chartDiv = document.createElement("div");
  chartDiv.setAttribute("id",chartId);
  textDiv = document.createElement("div");
  textDiv.setAttribute("id",textId);

  if (bigScreen) {
    mainDiv.setAttribute("class","mainPageTop");
    topSongsDiv.setAttribute("class","topSongsDiv " + topSongsClass);
    chartDiv.setAttribute("class","innerChartTopDiv " + chartClass);
    textDiv.setAttribute("class","innerTextTopDiv " + textClass);
    mainDiv.appendChild(topSongsDiv);
    mainDiv.appendChild(chartDiv);
    mainDiv.appendChild(textDiv);
  } else { // small screen (smartphone)
    mainDiv.setAttribute("class","mainPageSmall");
    topSongsDiv.setAttribute("class","topSongsDivSmall " + topSongsClass);
    chartDiv.setAttribute("class","innerChartTopDivSmall " + chartClass);
    textDiv.setAttribute("class","innerTextTopDivSmall " + textClass);
    mainDiv.appendChild(topSongsDiv);
    mainDiv.appendChild(chartDiv);
    mainDiv.appendChild(textDiv);
  }
}