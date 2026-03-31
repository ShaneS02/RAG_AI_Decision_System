import { useState } from "react";
import FileUpload from "./FileUpload";
import UrlUpload from "./UrlUpload";

import "./Upload.css";

const Upload = ({ uploadFile, uploadUrl }) => {
	const [activeTab, setActiveTab] = useState("file");

	return (
		<div className="upload-page">
			{/*tab section*/}
			<div className="tabs">
				<button
					className={activeTab === "file" ? "active" : ""}
					onClick={() => setActiveTab("file")}
				>
					FILE
				</button>

				<button
					className={activeTab === "url" ? "active" : ""}
					onClick={() => setActiveTab("url")}
				>
					URL
				</button>
			</div>

			{/* Content */}
			<div className="tab-content">
				{activeTab === "file" && <FileUpload uploadFile={uploadFile} />}
				{activeTab === "url" && <UrlUpload uploadUrl={uploadUrl} />}
			</div>
		</div>
	);
};

export default Upload;
