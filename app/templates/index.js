new Chart(document.getElementById("myChart"), {
    type: 'pie',
    data: {
      labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
        data: [2478,5267,734,784,433]
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Predicted world population (millions) in 2050'
      }
    }
});

var songs = {{ top_songs }}
console.log(songs[0])

var par = document.createElement("p");
var node = document.createTextNode('{{ top_songs[0][0] }}');
par.appendChild(node);
var element = document.getElementById("div1")
element.appendChild(par);
