import { useContext, useState } from "react";
import { ActiveAddDishContext } from "../../providers/ActiveAddDishProvider";
import { addItemAPI } from "../../services/addItemAPI";
import "./AddDish.scss";

export default function AddDish() {
	const { setActiveAddDish } = useContext(ActiveAddDishContext);
	const [name, setName] = useState("");
	const [price, setPrice] = useState(0);

	return (
		<div
			className="add-dish"
			onSubmit={e => {
				e.preventDefault();
				if (name || price) {
					addItemAPI({ name: name, price: price });
					setActiveAddDish(false);
				} else {
					alert("Введите данные");
				}
			}}
		>
			<form className="add-dish__form">
				<input
					value={name}
					onChange={e => setName(e.target.value)}
					className="add-dish__input"
					type="text"
					placeholder="Название"
				/>
				<input
					value={price}
					onChange={e => setPrice(e.target.value)}
					className="add-dish__input"
					type="number"
					placeholder="Цена"
				/>
				<div className="add-dish__btns">
					<button type="submit" className="add-dish__btn success">
						Добавить
					</button>
					<button
						type="button"
						className="add-dish__btn cancel"
						onClick={() => {
							setActiveAddDish(false);
						}}
					>
						Отмена
					</button>
				</div>
			</form>
		</div>
	);
}
