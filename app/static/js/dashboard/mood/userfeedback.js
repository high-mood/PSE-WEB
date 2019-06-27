
// var graph = document.querySelector("#graph");
// var dot = document.querySelector("#dot");
// var svg = d3.selectAll('#userfeedback-svg')

// var x = d3.scaleLinear().domain([-10, 10]).range([17, 203]);
// var y = d3.scaleLinear()
//     .domain([-10, 10])
//     .range([30, 150]);
// svg.append("g")
//     .attr("transform", "translate(-10,80)")
//     .call(d3.axisBottom(x));

// graph.addEventListener("click", getClickPosition, false);

// function getClickPosition(e) {
//     var parentPos = getPos(graph);
//     var xPos = e.clientX - parentPos.x - (dot.offsetWidth / 2);
//     var yPos = e.clientY - parentPos.y - (dot.offsetHeight / 2);

//     var translate3dValue = "translate3d(" + xPos + "px," + yPos + "px, 0)"
//     dot.style.transform = translate3dValue;
// }

// function getPos(element) {
//     var xPos = 0;
//     var yPos = 0;
//     while (element) {
//         xPos += (element.offsetLeft - element.scrollLeft + element.clientLeft);
//         yPos += (element.offsetTop - element.scrollTop + element.clientTop);
//         element = element.offsetParent;
//     }
//     if (!(xPos < 0 || yPos < 0 || xPos > 200 || yPos > 200)) {
//         return {
//             x: xPos,
//             y: yPos
//         };
//     }
// }

// function sendFeedback(el) {
//     var values = el.style.transform.split(/\w+\(|\);?/);
//     if (!values[1] || !values[1].length) {
//         return [];
//     }
//     return values[1].split(/,\s?/g).slice(0, 2);
// }


// var globaluserdata;

// function createSongRecommendationWidget(userid) {
//
//   var request = new XMLHttpRequest()
//
//   // request.open('GET', 'https://cors-anywhere.herokuapp.com/http://randomelements.nl/highmood/data/dummysonghistory.json', true)
//   request.open('GET', '/api/tracks/history/' + userid + '/0', true)
//
//   request.onload = function() {
//     var alldata = JSON.parse(this.response)
//     var userdata = alldata.resource
//     globaluserdata = userdata;
//
//
//     if (request.status >= 200 && request.status < 400) {
//
//       var songWidgetContainer = document.getElementById('Song-Recommendation');
//       var form = document.createElement('form')
//
//       songWidgetContainer.appendChild(form);
//
//       var length = userdata.songs.length;
//
//       if (length > 5) {
//         length = 5;
//       }
//
//       for (var i = 0; i < length; i++) {
//         var songdiv = document.createElement('div')
//         songdiv.classList.add('songdiv');
//         songdiv.id = userdata.songs[i].songid;
//
//         var songid = userdata.songs[i].songid;
//
//         var btn = document.createElement("BUTTON");
//         btn.innerHTML = "Select";
//         btn.setAttribute("type","button");
//         // btn.onclick = function(songid) { showSong(songid); };
//         btn.classList.add('SongRecButton');
//         songdiv.appendChild(btn);
//
//         var ifrm = document.createElement("iframe");
//         ifrm.setAttribute("src", "https://open.spotify.com/embed/track/" + userdata.songs[i].songid);
//         ifrm.setAttribute("align","left");
//         ifrm.style.width = "300px";
//         ifrm.style.height = "80px";
//
//         songdiv.appendChild(ifrm);
//         form.appendChild(songdiv)
//       }
//     }
//   }
//   request.send()
//
// }
