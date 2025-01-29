import { useContext, useEffect } from "react";
import "./App.scss";
import AddBtn from "./components/AddBtn/AddBtn";
import AddDish from "./components/AddDish/AddDish";
import AddOrder from "./components/AddOrder/AddOrder";
import ChoiceItems from "./components/AddOrder/ChoiceItems/ChoiceItems";
import ChangeStatus from "./components/ChangeStatus/ChangeStatus";
import FilterBtn from "./components/FilterOrders/FilterBtn";
import Header from "./components/Header/Header";
import Order from "./components/Order/Order";
import Search from "./components/Search/Search";
import { ActiveAddDishContext } from "./providers/ActiveAddDishProvider";
import { ActiveAddOrderContext } from "./providers/ActiveAddOrderProvider";
import { ActiveChangeStatusContext } from "./providers/ActiveChangeStatus";
import { ActiveChoiceItemsContext } from "./providers/ActiveChoiceItemsProvider";
import { OrdersContext } from "./providers/OrdersProvider";
import { getOrdersAPI } from "./services/getOrdersAPI";

export default function App() {
	const { orders, setOrders } = useContext(OrdersContext);
	const { activeAddOrder } = useContext(ActiveAddOrderContext);
	const { activeChoiceItems } = useContext(ActiveChoiceItemsContext);
	const { activeChangeStatus } = useContext(ActiveChangeStatusContext);
	const { activeAddDish } = useContext(ActiveAddDishContext);

	useEffect(() => {
		getOrdersAPI(setOrders);
	}, []);

	return (
		<div className="wrapper">
			<Header />
			<FilterBtn />
			<main className="content">
				<div className="container">
					<Search />
					<div className="content__orders">
						{orders.map(order => {
							return <Order key={order.id} order={order} />;
						})}
					</div>
				</div>
			</main>
			{activeAddOrder && <AddOrder />}
			{activeChoiceItems && <ChoiceItems />}
			{activeChangeStatus && <ChangeStatus />}
			{activeAddDish && <AddDish />}
			<AddBtn />
		</div>
	);
}
