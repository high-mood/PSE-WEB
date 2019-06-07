var songs = {{ songs }}
var count = {{count }}
new Chart(document.getElementById("barchart"), {
  type: 'bar',
  data: {
    labels: songs,
    datasets: [
      {
        label: "Count",
        data: count
      }
    ]
  },
  options: {
    legend: { display: false },
    title: {
      display: true,
      text: 'Top 10 most listened to songs'
    }
  }
});

console.log(songs);
console.log(count)
