import { Link } from "react-router-dom";
import { Navbar } from "./Navbar";
import { DarkThemeToggle } from "flowbite-react";
import '../../../public/css/header.css';
import AuthInfoComponent from "../auth/AuthInfoComponent";

export const Header = () => {
    // console.log('render header');

    return (
        <div className="header">
            <div className="logo-section ">
                <img src={"../favicon.ico"} alt={"TaskMane Logo"} width={50} height={50} />
                <Link to={'/'} className="home-link">
                    TaskMane
                </Link>
            </div>
            <div className="navbar-section ">
                <Navbar></Navbar>
            </div>
            <div className="auth-section ">
                <AuthInfoComponent />
                <DarkThemeToggle />
            </div>
        </div>
    );
}