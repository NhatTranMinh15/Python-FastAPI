import { message } from 'antd';
import { useFormik } from 'formik';
import { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import { LogInModel, LogInResponseModel } from '../../models/AuthModel';
import { checkToken, login } from '../../services/AuthService';


// Define the validation schema with Yup
const validationSchema = Yup.object({
    username: Yup.string()
        .required('Username is required'),
    password: Yup.string()
        .required('Password is required')
});

export const LoginComponent = () => {
    // console.log("render login");

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
                        navigate("/tasks")
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

    useEffect(() => {
        const token = sessionStorage.getItem('jwt_token')
        if (token) {
            const t = JSON.parse(token).access_token
            checkToken(t).then((response) => {
                const result: number = response.data
                if (result == 0) {
                    sessionStorage.removeItem('jwt_token')
                    navigate('/login')
                }
            })
        }
    }, [])

    return (
        <>
            {contextHolder}
            {sessionStorage.getItem("jwt_token") ?
                <Navigate to={"/tasks"}></Navigate>
                :
                <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-full lg:py-0">
                    <div className="p-6 space-y-4 md:space-y-6 sm:p-8 md:w-2/3 sm:w-full">
                        <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                            Sign in to your account
                        </h1>
                        <form className="space-y-4 md:space-y-6" onSubmit={formik.handleSubmit}>
                            <div>
                                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                                    Username
                                </label>
                                <input type="text" id="username" {...formik.getFieldProps('username')} className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="username" required={true} />
                                {formik.touched.username && formik.errors.username ? (
                                    <div className="text-red-600">{formik.errors.username}</div>
                                ) : null}
                            </div>
                            <div>
                                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                                    Password
                                </label>
                                <input type="password" id="password" placeholder="••••••••" {...formik.getFieldProps('password')} className="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required={true} />
                                {formik.touched.username && formik.errors.username ? (
                                    <div className="text-red-600">{formik.errors.username}</div>
                                ) : null}
                            </div>
                            <div className="flex items-center justify-between">
                                <div className="flex items-start">
                                    <div className="flex items-center h-5">
                                        <input id="remember" aria-describedby="remember" type="checkbox" className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800 hover:cursor-pointer" required={false} />
                                    </div>
                                    <div className="ml-3 text-sm">
                                        <label htmlFor='remember' className="text-gray-500 dark:text-gray-300 hover:cursor-pointer">
                                            Remember me
                                        </label>
                                    </div>
                                </div>
                                <Link to="#" className="text-sm font-medium text-primary-600 hover:underline dark:text-primary-500">
                                    Forgot password?
                                </Link>
                            </div>
                            <div className='flex justify-center'>
                                <button type="submit" className="button button-green">
                                    Login
                                </button>
                            </div>
                            <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                                Doesn’t have an account yet? {" "}
                                <Link to="/sign-up" className="font-medium text-primary-600 hover:underline dark:text-primary-500">
                                    Register here
                                </Link>
                            </p>
                        </form>
                    </div>
                </div>
            }
        </>
    );
};
