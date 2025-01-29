function updateItem(acc, item) {
	const itemIndex = acc.findIndex(i => i.id === item.id);
	if (itemIndex !== -1) {
		acc[itemIndex].count += 1;
	} else {
		acc.push({ ...item, count: 1 });
	}
	return acc;
}

function calculatePrice(item) {
	return { ...item, price: (item.price * item.count).toFixed(2) };
}

export function getUniqueItems(items) {
	let res = items.reduce((acc, item) => {
		return updateItem(acc, item);
	}, []);
	return res.map(item => calculatePrice(item));
}
