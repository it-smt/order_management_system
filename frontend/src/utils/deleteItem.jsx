export function deleteItem(e, id, setItems) {
	e.preventDefault();
	setItems(prevItems =>
		prevItems
			.map(item => {
				if (item.id === id) {
					if (item.count === 1) {
						return null;
					} else {
						return { ...item, count: item.count - 1 };
					}
				} else {
					return item;
				}
			})
			.filter(item => item !== null)
	);
}
