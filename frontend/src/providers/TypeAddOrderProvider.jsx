import { createContext, useState } from "react";

export const TypeAddOrderContext = createContext();

export function TypeAddOrderProvider({ children }) {
	const [typeAddOrder, setTypeAddOrder] = useState({});

	return (
		<TypeAddOrderContext.Provider value={{ typeAddOrder, setTypeAddOrder }}>
			{children}
		</TypeAddOrderContext.Provider>
	);
}
