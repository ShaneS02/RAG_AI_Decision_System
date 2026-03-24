import { useState, useRef } from "react";
import { Send, Loader } from "lucide-react";
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
		<div className="query-container" ref={containerRef}>
			<textarea
				className="query-input"
				ref={textareaRef}
				value={query}
				onChange={handleInput}
				placeholder="Type your text here..."
			/>
			<button
				className="query-button"
				onClick={handleSubmit}
				disabled={loading}
			>
				{loading ? (
					<Loader size={20} className="spin" />
				) : (
					<Send size={20} className="button-icon" />
				)}
			</button>
		</div>
	);
}
