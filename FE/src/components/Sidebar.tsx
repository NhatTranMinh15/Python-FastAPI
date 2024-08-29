import { Col, Nav, Row } from "react-bootstrap";
import {
    GlobalOutlined, UserOutlined, BarsOutlined
} from '@ant-design/icons';
import { Link } from "react-router-dom";
export const Sidebar = () => {
    return (
        <Nav defaultActiveKey="user" className="flex-column sidebar" style={{ position: 'sticky', top: "40%" }}>
            <Nav.Item>
                <Nav.Link as={Link} to={'/user/'} eventKey={"user"}>
                    <Row>
                        <Col sm={3}>
                            <UserOutlined className="nav-icon" />
                        </Col>
                        <Col>
                            User
                        </Col>
                    </Row>
                </Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link as={Link} to="/task/" eventKey={"task"}>
                    <Row>
                        <Col sm={3}>
                            <BarsOutlined className="nav-icon" />
                        </Col>
                        <Col>
                            Task
                        </Col>
                    </Row>
                </Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link as={Link} to={'/company/'} eventKey={"company"}>
                    <Row>
                        <Col sm={3}>
                            <GlobalOutlined className="nav-icon" />
                        </Col>
                        <Col>
                            Company
                        </Col>
                    </Row>
                </Nav.Link>
            </Nav.Item>
        </Nav>
    );
}