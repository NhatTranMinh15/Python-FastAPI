import { message } from 'antd';
import { useFormik } from 'formik';
import { useState } from 'react';
import { Button, Col, Container, Form, InputGroup, Row } from 'react-bootstrap';
import { Navigate, useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import { LogInModel, LogInResponseModel } from '../models/AuthModel';
import { login } from '../services/AuthService';


// Define the validation schema with Yup
const validationSchema = Yup.object({
    username: Yup.string()
        .required('Username is required'),
    password: Yup.string()
        .required('Password is required')
});

export const LogInComponent = () => {
    const [messageApi, contextHolder] = message.useMessage();
    const navigate = useNavigate();

    const [loading, setLoading] = useState<boolean>(false);

    const formik = useFormik({
        initialValues: {
            username: '',
            password: '',
        },
        validationSchema: validationSchema,
        onSubmit: async (values) => {
            const logInData: LogInModel = {
                username: values.username,
                password: values.password,
            };
            setLoading(true);
            await login(logInData)
                .then((res) => {
                    if (res.status == 200) {
                        const loginResponse: LogInResponseModel = {
                            token_type: res.data.token_type,
                            access_token: res.data.access_token
                        }
                        sessionStorage.setItem("jwt_token", JSON.stringify(loginResponse))
                        messageApi.success("Login Successfully", 2);
                        navigate("/task")
                    }
                })
                .catch((err) => {
                    setLoading(false);
                    if (err.response?.status === 401) {
                        messageApi.error('Wrong email or password');
                    }
                    if (err.response.status == 403) {
                        messageApi.error('You do not have permission to access this page!');
                    }
                });
        }
    });
    return (
        <Container fluid className='d-flex mt-5 mb-5 justify-content-center'>
            {contextHolder}
            {sessionStorage.getItem("jwt_token") ?
                <>
                    <Navigate to={"/task"}></Navigate>
                </>
                :
                <Form className="mx-5 border border-2 rounded-3 mt-5 mb-5" style={{ maxWidth: "60%", minWidth: "450px", textAlign: "left" }} onSubmit={formik.handleSubmit}>
                    <h3 className='px-5 py-3 fs-5 text-center border-bottom border-2'>
                        Login
                    </h3>
                    <Form.Group as={Row} className="mb-3 px-4 mt-4">
                        <Form.Label column sm={3} >
                            Username:<span className='mx-1'>*</span>
                        </Form.Label>
                        <Col sm={9}>
                            <Form.Control
                                type="text"
                                id="username"
                                className="password-onfocus"
                                {...formik.getFieldProps('username')}
                                aria-required
                            />
                            {formik.touched.username && formik.errors.username ? (
                                <div className="error-message">{formik.errors.username}</div>
                            ) : null}
                        </Col>
                    </Form.Group>
                    <Form.Group as={Row} className="mb-3 px-4">
                        <Form.Label column sm={3} >
                            Password:<span className='mx-1'>*</span>
                        </Form.Label>
                        <Col sm={9}>
                            <InputGroup className="password-onfocus" >
                                <Form.Control
                                    type={'password'}
                                    id="password"
                                    className="form-control"
                                    {...formik.getFieldProps('password')}
                                    aria-required
                                />
                            </InputGroup>
                            {formik.touched.password && formik.errors.password ? (
                                <div className="error-message">{formik.errors.password}</div>
                            ) : null}
                        </Col>
                    </Form.Group>
                    <Row>
                        <Col className="d-flex justify-content-end mb-3">
                            <Button
                                className="mx-4 text-white"
                                type="submit"
                                style={{ minWidth: "90px", border: 'none' }}
                                disabled={!formik.isValid || !formik.dirty || loading === true}>
                                Login
                            </Button>
                        </Col>
                    </Row>
                </Form>
            }
        </Container>
    );
};
