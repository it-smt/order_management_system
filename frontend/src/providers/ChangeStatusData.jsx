import { createContext, useState } from "react";

export const ChangeStatusDataContext = createContext();

export function ChangeStatusDataProvider({ children }) {
	const [changeStatusData, setChangeStatusData] = useState({});

	return (
		<ChangeStatusDataContext.Provider
			value={{ changeStatusData, setChangeStatusData }}
		>
			{children}
		</ChangeStatusDataContext.Provider>
	);
}
