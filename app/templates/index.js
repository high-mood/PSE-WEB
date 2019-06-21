var songs = {{ songs }}
var song_count = {{ song_count }}
var genres = {{ genres }}
var genre_count = {{ genre_count }}
// var timestamps = {{ timestamps }}
var duration = {{ duration }}

function randomColor() {
  return '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6)
}

var songs_colors = [];
var genres_colors = [];

for (var i in songs) {
  songs_colors.push(randomColor())
}

for (var i in genres) {
  genres_colors.push(randomColor())
}


function getTop10(divId) {
    // Establish the array which acts as a data source for the list
    var listData = [
        'Blue',
        'Red',
        'White',
        'Green',
        'Black',
        'Orange'
    ];

    // Make a container element for the list
    // var listContainer = document.createElement('div');
    var listContainer = document.getElementById(divId);

    // make the title/header
    var header = document.createElement('h4');
    header.innerHTML = "Your Top 10 Songs"
    header.setAttribute("style","text-align: center; font-size:40px; border-bottom: 2px solid pink;");
    header.id = "top10animeendings"
    listContainer.appendChild(header);

    // Make the list
    var listElement = document.createElement('ul');

    // listElement.classList.add('w3-ul w3-card-4')

    // Add it to the page
    listContainer.appendChild(listElement);
    // Set up a loop that goes through the items in listItems one at a time
    var numberOfListItems = songs.length;
    for (var i = 0; i < numberOfListItems; ++i) {
        // create an item for each one
        var listItem = document.createElement('li');

        // Add the item text
        listItem.innerHTML = songs[i]['name'];

        // Add listItem to the listElement
        listElement.appendChild(listItem);
    }
}

// Mounir's amazing first demo code <3

//new Chart(document.getElementById("barchart"), {
//  type: 'bar',
//  data: {
//    labels: songs,
//    datasets: [
//      {
//        label: "Count",
//        backgroundColor: songs_colors,
//        data: song_count
//      }
//    ]
//  },
//  options: {
//    legend: { display: false },
//    title: {
//      display: true,
//      text: 'Top 10 most listened to songs'
//    }
//  }
//});

//new Chart(document.getElementById("piechart"), {
//  type: 'pie',
//  data: {
//    labels: genres,
//    datasets: [{
//      label: "count",
//      backgroundColor: genres_colors,
//      data: genre_count
//    }]
//  },
//  options: {
//    title: {
//      display: true,
//      text: 'Your top 10 genres'
//    }
//  }
//});

//new Chart(document.getElementById("linechart"), {
//  type: 'line',
//  data: {
//    labels: timestamps,
//    datasets: [{
//        data: duration,
//        borderColor: "#0643a5",
//        label: "listen time (min)",
//        }]
//  },
//  options: {
//    title: {
//      display: true,
//      text: 'Total listening time over time'
//    }
//  }
//});
