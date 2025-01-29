import { useContext } from "react";
import { ActiveAddOrderContext } from "../../../providers/ActiveAddOrderProvider";
import { ItemsContext } from "../../../providers/ItemsProvider";
import { OrdersContext } from "../../../providers/OrdersProvider";
import { TableNumberContext } from "../../../providers/TableNumberProvider";
import { TypeAddOrderContext } from "../../../providers/TypeAddOrderProvider";
import { deleteOrderAPI } from "../../../services/deleteOrderAPI";
import { getUniqueItems } from "../../../utils/getUniqueItems";

export default function OrderHeader({ order }) {
	const { setOrders } = useContext(OrdersContext);
	const { setItems } = useContext(ItemsContext);
	const { setTableNumber } = useContext(TableNumberContext);
	const { setActiveAddOrder } = useContext(ActiveAddOrderContext);
	const { setTypeAddOrder } = useContext(TypeAddOrderContext);

	return (
		<div className="order__header">
			<h3 className="order__title">Заказ #{order.id}</h3>
			<div className="order__btns">
				<button
					onClick={() => {
						setTypeAddOrder({ type: "edit", order: order });
						setTableNumber(order.table_number);
						setItems(getUniqueItems(order.items));
						setActiveAddOrder(true);
					}}
					className="order__btn"
				>
					<img src="/img/icons/edit.svg" alt="" />
				</button>
				<button
					onClick={() => {
						deleteOrderAPI(order.id, setOrders);
					}}
					className="order__btn"
				>
					<img src="/img/icons/delete.svg" alt="" />
				</button>
			</div>
		</div>
	);
}
