import { createContext, useState } from "react";

export const TableNumberContext = createContext();

export function TableNumberProvider({ children }) {
	const [tableNumber, setTableNumber] = useState("");

	return (
		<TableNumberContext.Provider value={{ tableNumber, setTableNumber }}>
			{children}
		</TableNumberContext.Provider>
	);
}
