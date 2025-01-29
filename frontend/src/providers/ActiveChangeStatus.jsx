import { createContext, useState } from "react";

export const ActiveChangeStatusContext = createContext();

export function ActiveChangeStatusProvider({ children }) {
	const [activeChangeStatus, setActiveChangeStatus] = useState(false);

	return (
		<ActiveChangeStatusContext.Provider
			value={{ activeChangeStatus, setActiveChangeStatus }}
		>
			{children}
		</ActiveChangeStatusContext.Provider>
	);
}
