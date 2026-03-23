import { useState } from "react";

const UrlUpload = () => {
	const [url, setUrl] = useState("");

	const handleSubmit = () => {
		console.log(url);
	};

	return (
		<div className="upload-box">
			<div className="url-section">
				<input
					type="text"
					placeholder="Enter URL..."
					className="url-input"
					value={url}
					onChange={(e) => setUrl(e.target.value)}
				/>
				<button className="url-button" onClick={handleSubmit}>
					Upload
				</button>
			</div>
		</div>
	);
};

export default UrlUpload;
