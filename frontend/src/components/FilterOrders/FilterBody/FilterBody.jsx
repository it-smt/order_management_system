import { useContext, useState } from "react";
import { OrdersContext } from "../../../providers/OrdersProvider";
import { getOrdersAPI } from "../../../services/getOrdersAPI";
import "./FilterBody.scss";

export default function FilterBody({ setActiveFilter }) {
	const { setOrders } = useContext(OrdersContext);
	const [selectedOption, setSelectedOption] = useState(null);

	const handleOptionChange = changeEvent => {
		setSelectedOption(changeEvent.target.value);
	};

	const onSubmit = e => {
		e.preventDefault();
		getOrdersAPI(setOrders, null, selectedOption);
		setActiveFilter(false);
	};

	return (
		<div className="filter-body">
			<div className="filter-body__title">Фильтрация</div>
			<form className="filter-body__form" onSubmit={onSubmit}>
				<label>
					<input
						type="radio"
						value="В ожидании"
						checked={selectedOption === "В ожидании"}
						onChange={handleOptionChange}
					/>
					В ожидании
				</label>
				<label>
					<input
						type="radio"
						value="Готово"
						checked={selectedOption === "Готово"}
						onChange={handleOptionChange}
					/>
					Готово
				</label>
				<label>
					<input
						type="radio"
						value="Оплачено"
						checked={selectedOption === "Оплачено"}
						onChange={handleOptionChange}
					/>
					Оплачено
				</label>
				<button type="submit" className="filter-body__btn">
					Применить
				</button>
			</form>
		</div>
	);
}
