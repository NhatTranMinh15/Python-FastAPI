import { Link, useNavigate } from "react-router-dom";
import { Navbar } from "./Navbar";
export const Header = () => {
    const navigate = useNavigate()

    const logout = () => {
        sessionStorage.removeItem('jwt_token')
        navigate('/')
    }
    return (
        <div className="flex min-h-16">
            <div className="logo basis-1/2 sm:basis-4/12 md:basis-3/12  flex justify-center items-center">
                <img src={"/images/icon.png"} alt={"TaskMane Logo"} width={50} height={50}></img>
                <Link to={'/'} className="ml-3 font-mono text-xl text-stone-600 antialiased font-bold text-center">
                    TaskMane
                </Link>
            </div>
            <div className="between_space flex basis-1/12 sm:basis-7/12 md:basis-7/12 lg:basis-8/12 align-middle justify-center">
                <Navbar></Navbar>
            </div>
            <div className="auth basis-5/12 sm:basis-2/12  flex justify-center items-center">
                {sessionStorage.getItem('jwt_token') ?
                    <button className="py-2 px-5 border rounded-lg bg-emerald-400 hover:underline text-white hover:bg-emerald-600 duration-150" onClick={() => { logout() }}>
                        Logout
                    </button>
                    :
                    <Link to={"/login"} className="py-2 px-5 border rounded-lg bg-emerald-400 hover:underline text-white hover:bg-emerald-600 duration-150">
                        Login
                    </Link>
                }
            </div>
        </div>
    );
}