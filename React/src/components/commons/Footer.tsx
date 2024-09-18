import { Link } from "react-router-dom"

function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content text-center">
                <span  className=''>&copy; {new Date().getFullYear()} <Link to={"https://github.com/NhatTranMinh15/Python-FastAPI-Assignment"} >
                NhatTranMinh15
                </Link>
                . All rights reserved.</span >
            </div>
        </footer>)
}

export default Footer