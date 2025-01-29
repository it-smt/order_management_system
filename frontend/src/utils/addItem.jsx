export function addItem(e, item, items, setItems) {
	e.preventDefault();
	const itemIndex = items.findIndex(i => i.id === item.id);
	if (itemIndex !== -1) {
		setItems(prevItems => {
			const newItems = [...prevItems];
			newItems[itemIndex].count += 1;
			return newItems;
		});
	} else {
		setItems([...items, { id: item.id, name: item.name, count: 1 }]);
	}
}
