import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import App from './App.tsx'
import './index.css'
import { Error } from './components/Error.tsx';
import { Col, Container, Row } from 'react-bootstrap';
import { Sidebar } from './components/Sidebar.tsx';
import { Header } from './components/Header.tsx';
import { Footer } from './components/Footer.tsx';
import { UserComponent } from './components/UserComponent.tsx';
import { TaskComponent } from './components/TaskComponent.tsx';
import { CompanyComponent } from './components/CompanyComponent.tsx';
createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <Container style={{ maxWidth: '100%', width: 'auto', margin: 0 }}>
            <BrowserRouter>
                <Row>
                    <Header></Header>
                </Row>
                <Row>
                    <Col sm={2} style={{ borderRight: "black 1px solid"}}>
                        <Sidebar></Sidebar>
                    </Col>
                    <Col sm={10}>
                        <Container style={{ maxWidth: '100%', width: 'auto', margin: 0 }}>
                            <Routes>
                                <Route path='/' element={<App />} />
                                <Route path='/user' element={<UserComponent />} />
                                <Route path='/task' element={<TaskComponent />} />
                                <Route path='/company' element={<CompanyComponent />} />

                                <Route path='/*' element={<Error />} />
                            </Routes>
                        </Container>
                    </Col>
                </Row>
                <Row>
                    <Footer></Footer>
                </Row>
            </BrowserRouter>
        </Container>
    </StrictMode>,
)
