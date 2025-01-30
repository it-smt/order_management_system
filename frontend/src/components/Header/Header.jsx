import { useState } from "react";
import { StatisticsProvider } from "../../providers/StatisticsProvider";
import Statistics from "../Statistics/Statistics";
import "./Header.scss";

export default function Header() {
	const [activeStatistics, setActiveStatistics] = useState(false);
	return (
		<header className="header">
			<div className="container">
				<div className="header__row">
					<h2 className="header__logo">Order Management System</h2>
					<p
						onClick={() => {
							setActiveStatistics(true);
						}}
						className="header__info"
					>
						{"Выручка -> INFO"}
					</p>
					{activeStatistics && (
						<StatisticsProvider>
							<Statistics setActiveStatistics={setActiveStatistics} />
						</StatisticsProvider>
					)}
				</div>
			</div>
		</header>
	);
}
