import "./Home.css";
import QueryForm from "../components/QueryForm";
import ResponseViewer from "../components/ResponseViewer";

const Home = ({ handleQuery, queryResponse }) => {
	return (
		<div className="homePage">
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
