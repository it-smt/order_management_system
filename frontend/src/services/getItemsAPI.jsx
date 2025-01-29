export async function getItemsAPI(setChoiceItems) {
	await fetch("http://localhost:8000/api/v1/main/items")
		.then(res => res.json())
		.then(data => {
			setChoiceItems(data);
		})
		.catch(err => console.error(err));
}
