import { useState } from "react";

const UploadForm = () => {
	const [file, setFile] = useState(null);

	const handleUpload = async () => {
		const formData = new FormData();
		formData.append("file", file);

		await fetch("http://localhost:8000/upload", {
			method: "POST",
			body: formData,
		});
	};

	return (
		<div>
			<input
				type="file"
				accept=".pdf"
				onChange={(e) => setFile(e.target.files[0])}
			/>

			<button onClick={handleUpload}>Upload PDF</button>
		</div>
	);
};

export default UploadForm;
