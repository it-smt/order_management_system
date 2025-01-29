import { createContext, useState } from "react";

export const ActiveAddDishContext = createContext();

export function ActiveAddDishProvider({ children }) {
	const [activeAddDish, setActiveAddDish] = useState(false);

	return (
		<ActiveAddDishContext.Provider value={{ activeAddDish, setActiveAddDish }}>
			{children}
		</ActiveAddDishContext.Provider>
	);
}
