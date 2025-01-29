import { useContext, useState } from "react";
import { ActiveAddOrderContext } from "../../../providers/ActiveAddOrderProvider";
import { ActiveChoiceItemsContext } from "../../../providers/ActiveChoiceItemsProvider";
import { ItemsContext } from "../../../providers/ItemsProvider";
import { OrdersContext } from "../../../providers/OrdersProvider";
import AddedItems from "../../AddedItems/AddedItems";

export default function EditOrderForm() {
	const { orders, setOrders } = useContext(OrdersContext);
	const { setActiveAddOrder } = useContext(ActiveAddOrderContext);
	const { setActiveChoiceItems } = useContext(ActiveChoiceItemsContext);
	const { items, setItems } = useContext(ItemsContext);
	const [tableNumber, setTableNumber] = useState("");

	return (
		<form
			onSubmit={e => {
				e.preventDefault();
				// addOrderAPI(
				// 	tableNumber,
				// 	items,
				// 	setItems,
				// 	orders,
				// 	setOrders,
				// 	setActiveAddOrder
				// );
			}}
			className="add-order__form"
		>
			<input
				type="number"
				className="add-order__input"
				placeholder="Номер столика..."
				required
				value={tableNumber}
				onChange={e => setTableNumber(e.target.value)}
			/>
			<label className="add-order__label">
				<div className="add-order__label-actions">
					<h2 className="add-order__label-title">Блюда</h2>
					<button
						onClick={() => setActiveChoiceItems(true)}
						type="button"
						className="add-order__label-add"
					>
						+
					</button>
				</div>
				<AddedItems />
			</label>
			<button type="submit" className="add-order__submit">
				Добавить
			</button>
		</form>
	);
}
