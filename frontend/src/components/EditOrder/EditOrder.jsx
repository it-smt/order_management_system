import { useContext } from "react";
import { ActiveAddOrderContext } from "../../providers/ActiveAddOrderProvider";
import EditOrderForm from "../EditOrderForm/EditOrderForm";
import "./AddOrder.scss";

export default function EditOrder() {
	const { setActiveAddOrder } = useContext(ActiveAddOrderContext);

	return (
		<div className="add-order">
			<div className="add-order__header">
				<h1 className="add-order__title">Добавление заказа</h1>
				<p
					onClick={() => setActiveAddOrder(false)}
					className="add-order__close"
				>
					X
				</p>
			</div>
			<EditOrderForm />
		</div>
	);
}
