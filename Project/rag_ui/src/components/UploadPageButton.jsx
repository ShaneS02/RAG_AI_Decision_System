const UploadPageButton = ({ className, onClick, name }) => {
	return (
		<div>
			<button className={className} onClick={onClick}>
				{name}
			</button>
		</div>
	);
};

export default UploadPageButton;
