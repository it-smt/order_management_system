export async function changeOrderStatusAPI(orderId, orderStatus, setOrders) {
	await fetch(
		`http://localhost:8000/api/v1/main/orders/status?order_id=${orderId}&status=${orderStatus}`,
		{
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
			},
		}
	)
		.then(res => res.json())
		.then(data => {
			setOrders(prevOrders => {
				return prevOrders.map(order => {
					if (order.id === orderId) {
						return { ...order, status: orderStatus };
					}
					return order;
				});
			});
		})
		.catch(err => console.error(err));
}
