import {
	Route,
	createBrowserRouter,
	createRoutesFromElements,
	RouterProvider,
} from "react-router-dom";

import { useState } from "react";

import MainLayout from "./layouts/MainLayout";
import Home from "./pages/Home";
import Upload from "./pages/Upload";

function App() {
	const [response, setResponse] = useState("placeholder");
	const handleQuerySubmit = async (query) => {
		try {
			const res = await fetch("http://localhost:8000/analyze", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ text: query }),
			});
			const data = await res.json();
			setResponse(data);
		} catch (err) {
			setResponse({ error: err.message });
		}
	};

	const router = createBrowserRouter(
		createRoutesFromElements(
			<Route path="/" element={<MainLayout />}>
				<Route
					index
					element={
						<Home handleQuery={handleQuerySubmit} queryResponse={response} />
					}
				/>
				<Route path="/upload" element={<Upload />} />
			</Route>,
		),
	);

	return <RouterProvider router={router} />;
}

export default App;
