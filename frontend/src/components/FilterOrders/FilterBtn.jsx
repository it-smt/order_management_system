import { useState } from "react";
import "./FilterBody/FilterBody";
import FilterBody from "./FilterBody/FilterBody";
import "./FilterBtn.scss";

export default function FilterBtn() {
	const [activeFilter, setActiveFilter] = useState(false);

	return (
		<>
			<button
				onClick={() => setActiveFilter(activeFilter ? false : true)}
				type="button"
				className="filter-btn"
			>
				<img src="/img/icons/filter.svg" alt="" />
			</button>
			{activeFilter && <FilterBody setActiveFilter={setActiveFilter} />}
		</>
	);
}
