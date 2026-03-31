import { useState, ref, useRef } from "react";
import UploadPageButton from "../components/UploadPageButton";

const FileUpload = ({ uploadFile }) => {
	const [fileSelected, setFileSelected] = useState(null);
	const fileInputRef = useRef(null);

	const handleUploadSubmit = (e) => {
		uploadFile(fileSelected);
	};
	const handleClearSubmit = (e) => {
		setFileSelected(null);

		if (fileInputRef.current) {
			fileInputRef.current.value = "";
		}
	};

	const handleFileChange = (e) => {
		const file = e.target.files[0];
		if (!file) return;

		console.log(file);

		// Extra validation in addition to the accept
		const validTypes = [
			"application/pdf",
			"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
		];

		if (!validTypes.includes(file.type)) {
			alert("Only PDF and DOCX files are allowed.");
			return;
		}

		setFileSelected(file);
	};

	return (
		<div className="upload-box">
			<input
				type="file"
				id="fileUpload"
				className="file-input"
				ref={fileInputRef}
				onChange={handleFileChange}
			/>
			<label htmlFor="fileUpload" className="file-label">
				Choose File
			</label>

			{fileSelected && (
				<div className="file-selected">
					<p className="upload-file-message">
						Selected file: {fileSelected.name}
					</p>

					<div className="file-selected-buttons">
						<UploadPageButton
							className="file-upload-button"
							onClick={handleUploadSubmit}
							name={"Upload"}
						/>

						<UploadPageButton
							className="file-clear-button"
							onClick={handleClearSubmit}
							name={"Clear"}
						/>
					</div>
				</div>
			)}
		</div>
	);
};

export default FileUpload;
