function transformOrder(tableNumber, items) {
	return {
		table_number: tableNumber,
		items: items.flatMap(item => Array(item.count).fill({ id: item.id })),
	};
}

export async function editOrderAPI(id, tableNumber, items, setOrders) {
	console.log(items);
	const transformedOrder = transformOrder(tableNumber, items);
	await fetch(`http://localhost:8000/api/v1/main/orders?order_id=${id}`, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(transformedOrder),
	})
		.then(res => res.json())
		.then(data => {
			setOrders(prevOrders => {
				return prevOrders.map(prevOrder => {
					if (prevOrder.id === id) {
						return { ...prevOrder, ...data };
					}
					return prevOrder;
				});
			});
			console.log(data);
		})
		.catch(err => console.error(err));
}
