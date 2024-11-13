import axios from "axios";
import { ChangePasswordModel, LogInModel } from "../models/AuthModel";
import { URL, axiosConfig } from "../utils/Config";
import { message } from "antd";

export const login = async (data: LogInModel) => {
    const bodyFormData = new FormData();
    bodyFormData.append('username', data.username);
    bodyFormData.append('password', data.password);

    message.loading({ content: 'Logging in...', key: 'login' });
    const response = await axios.post(`${URL}/auth/token`, bodyFormData)
    message.destroy('login')
    return response
};
export const logout = async () => {
    message.loading({ content: 'Logging out...', key: 'logout' });
    const response = await axios.post(`${URL}/auth/logout`, null, axiosConfig());
    message.destroy('logout')
    return response;
}
export const changePassword = async (pswdData: ChangePasswordModel) => {
    message.loading({ content: 'Changing Password...', key: 'changePassword' });
    const response = await axios.patch(`${URL}/users/password`, pswdData, axiosConfig());
    message.destroy('changePassword');
    return response
};

export const checkToken = async (token: string) => {
    const response = await axios.post(`${URL}/auth/check`, token);
    return response
}