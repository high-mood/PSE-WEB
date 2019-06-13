function createHeatmapData(userData) {
//  console.log(userData)
  var songs = userData.moods;
  // console.log(songs)

  dataSet = []

  for (var i in d3.range(userData.moods.length)) {
    var song = songs[i];
    dataSet.push({name:"naam",data0:song.excitedness,data1:song.happiness});
  }

  // console.log(dataSet);

  return dataSet;

//  data = [{name:"bohemian rhapsody",data0:40,data1:60},{name:"Oya-lele",data0:40,data1:60},{name:"ode to joy",data0:20,data1:0},{name:"pokerface",data0:60,data1:0},{name:"symphony 7",data0:10,data1:10},{name:"imagine",data0:70,data1:30},{name:"Born to run",data0:70,data1:30}];
//  return data
}
