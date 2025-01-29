export async function getStatisticsAPI(setStatistics) {
	await fetch("http://localhost:8000/api/v1/main/statistics", {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
		},
	})
		.then(res => res.json())
		.then(data => {
			setStatistics(data);
		})
		.catch(err => console.error(err));
}
