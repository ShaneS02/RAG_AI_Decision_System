import { useState, useRef, use } from "react";
import "./QueryForm.css";

export default function QueryForm({ onSubmit }) {
	const [query, setQuery] = useState("");
	const textareaRef = useRef(null);
	const containerRef = useRef(null);
	const [loading, setLoading] = useState(false);

	const handleSubmit = async () => {
		if (!query) return;
		setLoading(true);
		await onSubmit(query);
		setLoading(false);
	};

	const handleInput = (e) => {
		setQuery(e.target.value);

		const textarea = textareaRef.current;
		const container = containerRef.current;

		if (textarea && container) {
			textarea.style.height = "auto"; // reset
			container.style.height = "auto"; // reset
			const newHeight = textarea.scrollHeight;
			textarea.style.height = textarea.scrollHeight + "px";
			container.style.height = newHeight + "px"; // container grows with textarea
		}
	};

	return (
		<div className="queryContainer" ref={containerRef}>
			<textarea
				className="queryInput"
				ref={textareaRef}
				value={query}
				onChange={handleInput}
				placeholder="Type your text here..."
			/>
			<button className="queryButton" onClick={handleSubmit} disabled={loading}>
				{loading ? "Loading..." : "Submit"}
			</button>
		</div>
	);
}
