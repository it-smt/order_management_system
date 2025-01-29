import { createContext, useState } from "react";

export const OrdersContext = createContext();

export function OrdersProvider({ children }) {
	const [orders, setOrders] = useState([]);

	return (
		<OrdersContext.Provider value={{ orders, setOrders }}>
			{children}
		</OrdersContext.Provider>
	);
}
