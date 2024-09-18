import { Link } from "react-router-dom";
import { Bars3Icon } from "@heroicons/react/24/outline";

export const Navbar = (
) => {
    return (
        <>
            <ul className="hidden sm:flex flex-row justify-center md:gap-10 ">
                <li className="side_li p-2 px-5 my-3 border-2 border-transparent">
                    <Link to="/tasks" className="flex">
                        <div className="w-full text-center ">
                            Tasks
                        </div>
                    </Link>
                </li>
                <li className="side_li p-2 px-5 my-3 border-2 border-transparent">
                    <Link to="/users" className="flex">
                        <div className="w-full text-center">
                            Users
                        </div>
                    </Link>
                </li>
                <li className="side_li p-2 px-5 my-3 border-2 border-transparent">
                    <Link to="/companies" className="flex">
                        <div className="w-full text-center">
                            Companies
                        </div>
                    </Link>
                </li>
            </ul>
            <button className="block sm:hidden m-auto">
                <Bars3Icon width={25}></Bars3Icon>
            </button>
        </>
    );
}