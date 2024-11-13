import { Link } from "react-router-dom"
const link = "https://github.com/NhatTranMinh15/Python-FastAPI-Assignment"
function Footer() {
    // console.log("render footer");
    return (
        <footer className="footer">
            <div className="footer-content text-center dark:text-white-smoke">
                <span className=''>
                    &copy; {new Date().getFullYear() + " "}
                    <Link to={link} >
                        NhatTranMinh15
                    </Link>
                    . All rights reserved.</span >
            </div>
        </footer>)
}

export default Footer