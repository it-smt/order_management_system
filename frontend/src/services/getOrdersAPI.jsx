export async function getOrdersAPI(
	setOrders,
	search = null,
	filterStatus = null
) {
	let link = "http://localhost:8000/api/v1/main/orders";
	if (search) {
		link += `?search=${search.trim()}`;
	}
	if (filterStatus) {
		if (link.includes("?")) {
			link += `&filter_status=${filterStatus.trim()}`;
		} else {
			link += `?filter_status=${filterStatus.trim()}`;
		}
	}
	await fetch(link, {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
		},
	})
		.then(response => response.json())
		.then(data => {
			setOrders(data);
		})
		.catch(err => console.error(err));
}
