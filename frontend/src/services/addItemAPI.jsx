export async function addItemAPI(item) {
	await fetch("http://localhost:8000/api/v1/main/items", {
		method: "POST",
		body: JSON.stringify(item),
	})
		.then(res => res.json())
		.catch(err => console.error(err));
}
