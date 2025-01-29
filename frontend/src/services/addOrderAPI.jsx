export async function addOrderAPI(
	tableNumber,
	items,
	orders,
	setOrders
) {
	await fetch("http://localhost:8000/api/v1/main/orders", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			table_number: tableNumber,
			items: items.flatMap(item => Array(item.count).fill({ id: item.id })),
		}),
	})
		.then(response => response.json())
		.then(data => {
			setOrders([data, ...orders]);
		})
		.catch(err => console.error(err));
}
