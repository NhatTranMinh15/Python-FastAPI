import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import { StrictMode } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import App from './App.tsx';
import { CompanyComponent } from './components/CompanyComponent.tsx';
import { Error } from './components/Error.tsx';
import { Footer } from './components/Footer.tsx';
import { Header } from './components/Header.tsx';
import { Sidebar } from './components/Sidebar.tsx';
import { TaskComponent } from './components/TaskComponent.tsx';
import { UserComponent } from './components/UserComponent.tsx';
import './index.css';
import { TaskDetailComponent } from './components/TaskDetailComponent.tsx';

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <Container style={{ maxWidth: '100%', width: 'auto', margin: 0 }}>
            <BrowserRouter>
                <Row>
                    <Header></Header>
                </Row>
                <Row>
                    <Col sm={2} style={{ borderRight: "black 1px solid", minWidth: "150px" }}>
                        <Sidebar></Sidebar>
                    </Col>
                    <Col sm={10}>
                        <Container style={{ maxWidth: '100%', width: 'auto', margin: 0, padding: 0 }}>
                            <Routes>
                                <Route path='/' element={<App />} />
                                <Route path='/user' element={<UserComponent />} />
                                <Route path='/task' element={<TaskComponent />} />
                                <Route path='/task/*' element={<TaskDetailComponent/>}/>
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
