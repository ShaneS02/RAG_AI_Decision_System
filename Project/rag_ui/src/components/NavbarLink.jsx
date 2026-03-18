import { NavLink } from "react-router-dom";
import "./NavbarLink.css";

const NavbarLink = ({ link, name }) => {
	return (
		<div>
			<NavLink className="navlink" to={link}>
				<span>{name}</span>
			</NavLink>
		</div>
	);
};

export default NavbarLink;
