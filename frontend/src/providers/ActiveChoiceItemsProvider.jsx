import { createContext, useState } from "react";

export const ActiveChoiceItemsContext = createContext();

export function ActiveChoiceItemsProvider({ children }) {
	const [activeChoiceItems, setActiveChoiceItems] = useState(false);

	return (
		<ActiveChoiceItemsContext.Provider
			value={{ activeChoiceItems, setActiveChoiceItems }}
		>
			{children}
		</ActiveChoiceItemsContext.Provider>
	);
}
