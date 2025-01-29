import { useContext } from "react";
import { ItemsContext } from "../../../../providers/ItemsProvider";
import { addItem } from "../../../../utils/addItem";
import "./ChoiceItem.scss";

export default function ChoiceItem({ item }) {
	const { items, setItems } = useContext(ItemsContext);

	return (
		<li className="add-items__item">
			<div className="add-items__item-name">
				{item.name} {item.price} ₽
			</div>
			<button
				type="button"
				className="add-items__item-btn"
				onClick={e => addItem(e, item, items, setItems)}
			>
				+
			</button>
		</li>
	);
}
