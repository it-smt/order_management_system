import { useContext, useEffect, useState } from "react";
import { ActiveChoiceItemsContext } from "../../../providers/ActiveChoiceItemsProvider";
import { getItemsAPI } from "../../../services/getItemsAPI";
import ChoiceItem from "./ChoiceItem/ChoiceItem";
import "./ChoiceItems.scss";

export default function ChoiceItems() {
	const { setActiveChoiceItems } = useContext(ActiveChoiceItemsContext);
	const [choiceItems, setChoiceItems] = useState([]);

	useEffect(() => {
		getItemsAPI(setChoiceItems);
	}, []);

	return (
		<div className="add-items">
			<div className="add-items__header">
				<div
					onClick={() => setActiveChoiceItems(false)}
					className="add-items__back"
				>
					<img src="/img/icons/back.svg" alt="" />
				</div>
				<div className="add-items__title">Выбор блюд</div>
			</div>
			<div className="add-items__items">
				{choiceItems.map((item, i) => {
					return <ChoiceItem key={i} item={item} />;
				})}
			</div>
		</div>
	);
}
