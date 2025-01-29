import { createContext, useState } from "react";

export const ActiveAddOrderContext = createContext();

export function ActiveAddOrderProvider({ children }) {
	const [activeAddOrder, setActiveAddOrder] = useState(false);

	return (
		<ActiveAddOrderContext.Provider
			value={{ activeAddOrder, setActiveAddOrder }}
		>
			{children}
		</ActiveAddOrderContext.Provider>
	);
}
