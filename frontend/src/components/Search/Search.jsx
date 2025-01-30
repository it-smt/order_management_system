import { useContext, useState } from "react";
import { OrdersContext } from "../../providers/OrdersProvider";
import { getOrdersAPI } from "../../services/getOrdersAPI";
import "./Search.scss";

export default function Search() {
	const { setOrders } = useContext(OrdersContext);
	const [value, setValue] = useState("");

	const onSubmit = e => {
		e.preventDefault();
		getOrdersAPI(setOrders, value, null);
	};

	return (
		<div className="search">
			<form className="search__form" onSubmit={onSubmit}>
				<input
					type="text"
					className="search__input"
					value={value}
					onChange={e => setValue(e.target.value)}
				/>
				<button className="search__button" type="submit">
					<img src="/img/icons/search.svg" alt="" />
				</button>
			</form>
		</div>
	);
}
