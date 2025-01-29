import { useContext } from "react";
import { ActiveChangeStatusContext } from "../../providers/ActiveChangeStatus";
import { ChangeStatusDataContext } from "../../providers/ChangeStatusData";
import { getUniqueItems } from "../../utils/getUniqueItems";
import Item from "./Item/Item";
import "./Order.scss";
import OrderHeader from "./OrderHeader/OrderHeader";

export default function Order({ order }) {
	const { setActiveChangeStatus } = useContext(ActiveChangeStatusContext);
	const { setChangeStatusData } = useContext(ChangeStatusDataContext);

	return (
		<div className="content__order order">
			<h1 className="order__table">Столик: {order.table_number}</h1>
			<OrderHeader order={order} />
			<div className="order__body">
				<ul className="order__items">
					{getUniqueItems(order.items).map((item, i) => {
						return <Item key={i} item={item} />;
					})}
				</ul>
			</div>
			<div className="order__footer">
				<p className="order__status">
					{order.status}{" "}
					<img
						onClick={() => {
							setChangeStatusData({
								orderId: order.id,
								orderStatus: order.status,
							});
							setActiveChangeStatus(true);
						}}
						src="/img/icons/change.svg"
						alt=""
					/>
				</p>
				<div className="order__total-price">Итого: {order.total_price} ₽</div>
			</div>
		</div>
	);
}
