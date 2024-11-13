import { Link } from "react-router-dom";
import { Bars3Icon } from "@heroicons/react/24/outline";

export const Navbar = () => {
  // console.log("Render Navbar");
  
  return (
    <>
      <ul className="navbar">
        <li className="nav-li ">
          <Link to="/tasks" className="flex">
            <div className="w-full text-center ">
              Tasks
            </div>
          </Link>
        </li>
        <li className="nav-li ">
          <Link to="/users" className="flex">
            <div className="w-full text-center">
              Users
            </div>
          </Link>
        </li>
        <li className="nav-li ">
          <Link to="/companies" className="flex">
            <div className="w-full text-center">
              Companies
            </div>
          </Link>
        </li>
      </ul>
      <button className="block sm:hidden m-auto dark:text-white duration-200">
        <Bars3Icon width={25}></Bars3Icon>
      </button>
    </>
  );
}