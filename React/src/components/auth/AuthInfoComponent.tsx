import { Link, useNavigate } from "react-router-dom"

const AuthInfoComponent = () => {

    const navigate = useNavigate()

    const logout = () => {
        sessionStorage.removeItem('jwt_token')
        navigate('/')
    }

    return sessionStorage.getItem('jwt_token') ?
        <button className=" button button-green" onClick={() => { logout() }}>
            Logout
        </button>
        :
        <Link to={"/login"} className="button button-green">
            Login
        </Link>


}

export default AuthInfoComponent