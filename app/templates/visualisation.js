new Chart(document.getElementById("myChart"), {
	type: 'pie',
	data: {
		labels: ["hi1", "hi2", "hi3"],
		datasets: [{
			label: "testlabel (seconds)",
			backgroundColor["red", "blue", "green"],
			data: [1, 2, 3]
		}]
	},
	options: {
		title: {
			display: true,
			text: 'sample text'
		}
	}
});
