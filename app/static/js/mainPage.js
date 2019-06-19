function createMainPageChart(mainPageDiv,chartId,chartClass,textId,textClass,even,bigScreen) {

  mainDiv = document.getElementById(mainPageDiv);

  chartDiv = document.createElement("div");
  chartDiv.setAttribute("id",chartId);
  textDiv = document.createElement("div");
  textDiv.setAttribute("id",textId);

  if (bigScreen) { // TODO select if big screen
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
    chartDiv.setAttribute("class","innerChartDivSmall" + chartClass);
    textDiv.setAttribute("class","innerTextDivSmall" + textClass);
    mainDiv.appendChild(chartDiv);
    mainDiv.appendChild(textDiv);
  }
}