import "./ResponseViewer.css";

const ResponseViewer = ({ response }) => {
	if (!response) return null;

	return (
		<div className="container">
			<pre className="response"> {JSON.stringify(response, null, 2)} </pre>
		</div>
	);
};

export default ResponseViewer;
