import { useContext } from "react";
import { ItemsContext } from "../../../../providers/ItemsProvider";
import { deleteItem } from "../../../../utils/deleteItem";

export default function AddedItem({ item }) {
	const { setItems } = useContext(ItemsContext);

	return (
		<li className="add-order__item item">
			<div className="item__name">
				{item.name} x{item.count}
			</div>
			<button
				type="button"
				className="item__btn"
				onClick={e => deleteItem(e, item.id, setItems)}
			>
				-
			</button>
		</li>
	);
}
