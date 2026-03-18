import "./Navbar.css";
import NavbarLink from "./NavbarLink";

const Navbar = () => {
	return (
		<nav className="navbar">
			<div className="navbar-container">
				<div className="navbar-inner">
					<div className="navbar-left"></div>

					<NavbarLink link={"/"} name={"Home"} />
					<NavbarLink link={"/upload"} name={"Upload"} />
				</div>
			</div>
		</nav>
	);
};

export default Navbar;
