import { useContext } from "react";
import { ActiveChangeStatusContext } from "../../providers/ActiveChangeStatus";
import { ChangeStatusDataContext } from "../../providers/ChangeStatusData";
import { OrdersContext } from "../../providers/OrdersProvider";
import { changeOrderStatusAPI } from "../../services/changeOrderStatusAPI";
import "./ChangeStatus.scss";

export default function ChangeStatus() {
	const { setActiveChangeStatus } = useContext(ActiveChangeStatusContext);
	const { changeStatusData, setChangeStatusData } = useContext(
		ChangeStatusDataContext
	);
	const { setOrders } = useContext(OrdersContext);

	const handleChange = event => {
		setChangeStatusData({
			orderId: changeStatusData.orderId,
			orderStatus: event.target.value,
		});
	};

	return (
		<div className="change-status">
			<form
				className="change-status__form"
				onSubmit={e => {
					e.preventDefault();
					changeOrderStatusAPI(
						changeStatusData.orderId,
						changeStatusData.orderStatus,
						setOrders
					);
					setActiveChangeStatus(false);
				}}
			>
				<select
					className="change-status__select"
					value={changeStatusData.orderStatus}
					onChange={handleChange}
				>
					<option className="change-status__option" value="В ожидании">
						В ожидании
					</option>
					<option className="change-status__option" value="Готово">
						Готово
					</option>
					<option className="change-status__option" value="Оплачено">
						Оплачено
					</option>
				</select>
				<div className="change-status__btns">
					<button className="change-status__btn success" type="submit">
						Изменить
					</button>
					<button
						onClick={() => setActiveChangeStatus(false)}
						className="change-status__btn cancel"
						type="button"
					>
						Отмена
					</button>
				</div>
			</form>
		</div>
	);
}
