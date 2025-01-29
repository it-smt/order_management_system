import { createContext, useState } from "react";

export const ItemsContext = createContext();

export function ItemsProvider({ children }) {
	const [items, setItems] = useState([]);

	return (
		<ItemsContext.Provider value={{ items, setItems }}>
			{children}
		</ItemsContext.Provider>
	);
}
