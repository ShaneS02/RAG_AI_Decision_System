const FileUpload = () => {
	const handleFileChange = (e) => {
		const file = e.target.files[0];
		console.log(file);
	};

	return (
		<div className="upload-box">
			<input
				type="file"
				id="fileUpload"
				className="file-input"
				onChange={handleFileChange}
			/>
			<label htmlFor="fileUpload" className="file-label">
				Choose File
			</label>
		</div>
	);
};

export default FileUpload;
