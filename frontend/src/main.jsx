import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./null.scss";
import { ActiveAddDishProvider } from "./providers/ActiveAddDishProvider.jsx";
import { ActiveAddOrderProvider } from "./providers/ActiveAddOrderProvider.jsx";
import { ActiveChangeStatusProvider } from "./providers/ActiveChangeStatus.jsx";
import { ActiveChoiceItemsProvider } from "./providers/ActiveChoiceItemsProvider.jsx";
import { ChangeStatusDataProvider } from "./providers/ChangeStatusData.jsx";
import { ItemsProvider } from "./providers/ItemsProvider.jsx";
import { OrdersProvider } from "./providers/OrdersProvider.jsx";
import { TableNumberProvider } from "./providers/TableNumberProvider.jsx";
import { TypeAddOrderProvider } from "./providers/TypeAddOrderProvider.jsx";

createRoot(document.getElementById("root")).render(
	<StrictMode>
		<OrdersProvider>
			<ActiveAddOrderProvider>
				<TableNumberProvider>
					<TypeAddOrderProvider>
						<ActiveChoiceItemsProvider>
							<ItemsProvider>
								<ChangeStatusDataProvider>
									<ActiveChangeStatusProvider>
										<ActiveAddDishProvider>
											<App />
										</ActiveAddDishProvider>
									</ActiveChangeStatusProvider>
								</ChangeStatusDataProvider>
							</ItemsProvider>
						</ActiveChoiceItemsProvider>
					</TypeAddOrderProvider>
				</TableNumberProvider>
			</ActiveAddOrderProvider>
		</OrdersProvider>
	</StrictMode>
);
