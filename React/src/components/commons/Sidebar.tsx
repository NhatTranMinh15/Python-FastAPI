import { BuildingOffice2Icon, ClipboardDocumentListIcon, HomeIcon, UsersIcon } from "@heroicons/react/24/outline";
import { Link } from "react-router-dom";

export const Sidebar = (
) => {
    return (
        <div className="sticky top-40%">
            <ul className="text-center">
                <li className="side_li p-2 my-3 border-2 border-transparent">
                    <Link to="/" className="flex">
                        <HomeIcon width={25} />
                        <div className="w-full text-center">
                            Home
                        </div>
                    </Link>
                </li>
                <li className="side_li p-2 my-3 border-2 border-transparent">
                    <Link to="/tasks" className="flex">
                        <ClipboardDocumentListIcon width={25} />
                        <div className="w-full text-center ">
                            Tasks
                        </div>
                    </Link>
                </li>
                <li className="side_li p-2 my-3 border-2 border-transparent">
                    <Link to="/users" className="flex">
                        <UsersIcon width={25} />
                        <div className="w-full text-center">
                            Users
                        </div>
                    </Link>
                </li>
                <li className="side_li p-2 my-3 border-2 border-transparent">
                    <Link to="/companies" className="flex">
                        <BuildingOffice2Icon width={25} />
                        <div className="w-full text-center">
                            Companies
                        </div>
                    </Link>
                </li>
            </ul>
        </div>
    );
}