import { useContext, useEffect, useState } from "react";
import { ItemsContext } from "../../../providers/ItemsProvider";
import AddedItem from "./AddedItem/AddedItem";

export default function AddedItems() {
	const { items } = useContext(ItemsContext);
	const [itemsState, setItemsState] = useState(items);

	useEffect(() => {
		setItemsState(items);
	}, [items]);

	return (
		<ul className="add-order__items">
			{itemsState.map(item => {
				return <AddedItem key={item.id} item={item} />;
			})}
		</ul>
	);
}
