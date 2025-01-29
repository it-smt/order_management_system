import { createContext, useState } from "react";

export const StatisticsContext = createContext();

export function StatisticsProvider({ children }) {
	const [statistics, setStatistics] = useState({});

	return (
		<StatisticsContext.Provider value={{ statistics, setStatistics }}>
			{children}
		</StatisticsContext.Provider>
	);
}
