import { useState } from "react";

export default function QueryForm({ onSubmit }) {
	const [query, setQuery] = useState("");
	const [loading, setLoading] = useState(false);

	const handleSubmit = async () => {
		if (!query) return;
		setLoading(true);
		await onSubmit(query);
		setLoading(false);
	};

	return (
		<div>
			<textarea
				rows={6}
				style={{ width: "100%", padding: "10px" }}
				value={query}
				onChange={(e) => setQuery(e.target.value)}
				placeholder="Type your text here..."
			/>
			<button
				onClick={handleSubmit}
				disabled={loading}
				style={{ marginTop: "10px", padding: "10px 20px" }}
			>
				{loading ? "Loading..." : "Submit"}
			</button>
		</div>
	);
}
