import Navbar from "../components/Navbar";
import { Outlet } from "react-router-dom";

const MainLayout = () => {
	return (
		<>
			{/*Navbar Component in Navbar.jsx*/}
			<Navbar />
			<Outlet />
		</>
	);
};

export default MainLayout;
