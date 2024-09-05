import { Button, Container } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

export const Header = () => {
    const navigate = useNavigate()
    const logout = () => {
        sessionStorage.removeItem("jwt_token")
        navigate('/')
    }
    return (
        <Container style={{ borderBottom: "1px black solid" }}>
            <h1>
                Header
            </h1>
            <Button onClick={() => { logout(); }}>Log out</Button>
        </Container>
    );
}