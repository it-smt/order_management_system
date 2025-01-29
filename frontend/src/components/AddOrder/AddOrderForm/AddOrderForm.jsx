import { useContext } from "react";
import { ActiveAddOrderContext } from "../../../providers/ActiveAddOrderProvider";
import { ActiveChoiceItemsContext } from "../../../providers/ActiveChoiceItemsProvider";
import { ItemsContext } from "../../../providers/ItemsProvider";
import { OrdersContext } from "../../../providers/OrdersProvider";
import { TableNumberContext } from "../../../providers/TableNumberProvider";
import { TypeAddOrderContext } from "../../../providers/TypeAddOrderProvider";
import { addOrderAPI } from "../../../services/addOrderAPI";
import { editOrderAPI } from "../../../services/editOrderAPI";
import { getUniqueItems } from "../../../utils/getUniqueItems";
import AddedItems from "../AddedItems/AddedItems";

export default function AddOrderForm() {
	const { orders, setOrders } = useContext(OrdersContext);
	const { setActiveAddOrder } = useContext(ActiveAddOrderContext);
	const { setActiveChoiceItems } = useContext(ActiveChoiceItemsContext);
	const { items, setItems } = useContext(ItemsContext);
	const { tableNumber, setTableNumber } = useContext(TableNumberContext);
	const { typeAddOrder } = useContext(TypeAddOrderContext);

	function submitForm(e) {
		e.preventDefault();
		if (typeAddOrder.type == "edit") {
			setItems(getUniqueItems(typeAddOrder.order.items));
			editOrderAPI(typeAddOrder.order.id, tableNumber, items, setOrders);
		} else {
			addOrderAPI(tableNumber, items, orders, setOrders);
		}
		setActiveAddOrder(false);
		setItems([]);
	}

	return (
		<form onSubmit={e => submitForm(e)} className="add-order__form">
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
				{typeAddOrder.type == "edit" ? "Изменить" : "Добавить"}
			</button>
		</form>
	);
}
