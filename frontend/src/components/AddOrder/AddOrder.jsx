import { useContext } from "react";
import { ActiveAddOrderContext } from "../../providers/ActiveAddOrderProvider";
import { TypeAddOrderContext } from "../../providers/TypeAddOrderProvider";
import "./AddOrder.scss";
import AddOrderForm from "./AddOrderForm/AddOrderForm";

export default function AddOrder() {
	const { setActiveAddOrder } = useContext(ActiveAddOrderContext);
	const { typeAddOrder } = useContext(TypeAddOrderContext);

	return (
		<div className="add-order">
			<div className="add-order__header">
				<h1 className="add-order__title">
					{typeAddOrder.type == "edit"
						? "Редактирование заказа"
						: "Добавление заказа"}
				</h1>
				<p
					onClick={() => setActiveAddOrder(false)}
					className="add-order__close"
				>
					X
				</p>
			</div>
			<AddOrderForm />
		</div>
	);
}
