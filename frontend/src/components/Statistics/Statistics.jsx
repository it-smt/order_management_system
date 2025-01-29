import { useContext, useEffect } from "react";
import { StatisticsContext } from "../../providers/StatisticsProvider";
import { getStatisticsAPI } from "../../services/getStatisticsAPI";
import "./Statistics.scss";

export default function Statistics({ setActiveStatistics }) {
	const { statistics, setStatistics } = useContext(StatisticsContext);

	useEffect(() => {
		getStatisticsAPI(setStatistics);
	}, []);

	return (
		<div className="statistics">
			<h1 className="statistics__title">
				Статистика <span onClick={() => setActiveStatistics(false)}>X</span>
			</h1>
			<h2 className="statistics__total-revenue">
				Общая выручка: {statistics.total_revenue} ₽
			</h2>
			<div className="number-orders">
				<h3 className="number-orders__title">Количество заказов</h3>
				<div className="number-orders__grid">
					<div className="number-orders__column-title">В ожидании</div>
					<div className="number-orders__column-title">Готово</div>
					<div className="number-orders__column-title">Оплачено</div>
					<div className="number-orders__quantity">
						{statistics.count_waiting}
					</div>
					<div className="number-orders__quantity">{statistics.count_done}</div>
					<div className="number-orders__quantity">
						{statistics.count_payed}
					</div>
				</div>
			</div>
		</div>
	);
}
