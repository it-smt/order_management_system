export async function deleteOrderAPI(orderId, setOrders) {
	await fetch(`http://localhost:8000/api/v1/main/orders?order_id=${orderId}`, {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json",
		},
	})
		.then(response => response.json())
		.then(data => {
			if (!("detail" in data)) {
				setOrders(prevOrders =>
					prevOrders.filter(prevOrder => prevOrder.id !== orderId)
				);
			}
		})
		.catch(err => console.log(err));
}
