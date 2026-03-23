import "./Home.css";
import QueryForm from "../components/QueryForm";
import ResponseViewer from "../components/ResponseViewer";

const Home = ({ handleQuery, queryResponse }) => {
	return (
		<div className="homePage">
			{/* DRAFT OF PAGE CHANGES*/}

			{/* LEFT SIDE IS A SIDEBAR */}

			{/* RIGHT IS A BLANK AREA WHOSE BEHAVIOR WILL CHANGE WITH SECTIONS DISPLAYED */}

			{/* RESPONSE VIEWER WILL NOT BE ACTIVE UNLESS THERE IS SOMETHING TO SHOW */}

			{/* QUERY FORM WILL BE ALGIN IN THE CENTER IF RESPONSE VIEWER IS NOT ACTIVE 
				ELSE HAVE IT ATTACHED TO THE BOTTOM OF THAT SECTION
			*/}

			{/* NAVBAR SHOULD BE ATTAHCHED TO THE TOP SO IT IS STILL VISIBLE WHEN SCROLLING */}

			<span className="responseViewer">
				<ResponseViewer response={queryResponse} />
			</span>
			<span className="querForm">
				<QueryForm onSubmit={handleQuery} />
			</span>
		</div>
	);
};

export default Home;
