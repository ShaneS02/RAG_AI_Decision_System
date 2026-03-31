import { useState } from "react";
import UploadPageButton from "../components/UploadPageButton";

const UrlUpload = ({ uploadUrl }) => {
	const [url, setUrl] = useState("");

	const handleSubmit = () => {
		uploadUrl(url);
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
				<UploadPageButton
					className="url-button"
					onClick={handleSubmit}
					name={"Upload"}
				/>
			</div>
		</div>
	);
};

export default UrlUpload;
