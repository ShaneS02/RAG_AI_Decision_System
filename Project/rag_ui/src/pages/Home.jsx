import "./Home.css";
import QueryForm from "../components/QueryForm";
import ResponseViewer from "../components/ResponseViewer";

const Home = ({ handleQuery, queryResponse }) => {
	const hasResponse = !!queryResponse;

	return (
		<div className="home">
			{/* DRAFT OF PAGE CHANGES*/}

			{/* LEFT SIDE IS A SIDEBAR */}
			<div className="sidebar">
				<div className="sidebar-header">
					<h2>Chats</h2>
				</div>

				<div className="chat-list">
					<div className="chat-item">Chat 1</div>
				</div>
			</div>

			{/* RIGHT IS A BLANK AREA WHOSE BEHAVIOR WILL CHANGE WITH SECTIONS DISPLAYED */}
			<div
				className={`main-content ${hasResponse ? "has-response" : "no-response"}`}
			>
				{/* RESPONSE VIEWER WILL NOT BE ACTIVE UNLESS THERE IS SOMETHING TO SHOW */}
				{hasResponse && (
					<div className="response-viewer">
						<ResponseViewer response={queryResponse} />
					</div>
				)}

				{/* QUERY FORM WILL BE ALGIN IN THE CENTER IF RESPONSE VIEWER IS NOT ACTIVE 
				ELSE HAVE IT ATTACHED TO THE BOTTOM OF THAT SECTION
				*/}

				<div className={`query-form ${hasResponse ? "bottom" : "center"}`}>
					<QueryForm onSubmit={handleQuery} />
				</div>
			</div>
		</div>
	);
};

export default Home;
