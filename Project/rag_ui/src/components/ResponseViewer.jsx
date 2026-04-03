import "./ResponseViewer.css";

const ResponseViewer = ({ response }) => {
	if (!response) return null;
	console.log("Response Viewer: ", response);

	return (
		<div className="container">
			<pre className="response"> {JSON.stringify(response, null, 2)} </pre>
		</div>
	);
};

export default ResponseViewer;
