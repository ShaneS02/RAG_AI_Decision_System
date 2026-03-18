import "./Home.css";
import QueryForm from "../components/QueryForm";
import ResponseViewer from "../components/ResponseViewer";

const Home = ({ handleQuery, queryResponse }) => {
	return (
		<div className="homePage">
			<ResponseViewer response={queryResponse} />
			<QueryForm onSubmit={handleQuery} />
		</div>
	);
};

export default Home;
