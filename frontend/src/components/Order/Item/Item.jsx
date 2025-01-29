export default function Item({ item }) {
	return (
		<li className="order__item">
			<p className="order__item-name">
				{item.name} <span>x{item.count}</span>
			</p>
			<p className="order__item-price">{item.price} ₽</p>
		</li>
	);
}
