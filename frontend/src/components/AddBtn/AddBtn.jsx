import { useContext, useState } from "react";
import { ActiveAddDishContext } from "../../providers/ActiveAddDishProvider";
import { ActiveAddOrderContext } from "../../providers/ActiveAddOrderProvider";
import { TypeAddOrderContext } from "../../providers/TypeAddOrderProvider";
import "./AddBtn.scss";

export default function AddBtn() {
	const { setTypeAddOrder } = useContext(TypeAddOrderContext);
	const { setActiveAddOrder } = useContext(ActiveAddOrderContext);
	const { setActiveAddDish } = useContext(ActiveAddDishContext);
	const [activeAddBtn, setActiveAddBtn] = useState(false);

	return (
		<>
			<button
				onClick={() => setActiveAddBtn(activeAddBtn ? false : true)}
				className="add-btn"
			></button>
			{activeAddBtn && (
				<div className="add-btn__body">
					<ul className="add-btn__list">
						<li
							onClick={() => {
								setActiveAddOrder(true);
								setActiveAddBtn(false);
								setTypeAddOrder({});
							}}
							className="add-btn__item"
						>
							Добавить заказ
						</li>
						<li
							onClick={() => {
								setActiveAddDish(true);
								setActiveAddBtn(false);
							}}
							className="add-btn__item"
						>
							Добавить блюдо
						</li>
					</ul>
				</div>
			)}
		</>
	);
}
