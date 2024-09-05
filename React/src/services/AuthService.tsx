import axios from "axios";
import { ChangePasswordModel, LogInModel } from "../models/AuthModel";
import { API, axiosConfig } from "../utils/Config";
import { message } from "antd";

export const login = async (data: LogInModel) => {
    const bodyFormData = new FormData();
    bodyFormData.append('username', data.username);
    bodyFormData.append('password', data.password);

    message.loading({ content: 'Logging in...', key: 'login' });
    const response = await axios.post(`${API}/auth/login`, bodyFormData)
    message.destroy('login')
    return response
};
export const logout = async () => {
    message.loading({ content: 'Logging out...', key: 'logout' });
    const response = await axios.post(`${API}/auth/logout`, null, axiosConfig());
    message.destroy('logout')
    return response;
}
export const changePassword = async (pswdData: ChangePasswordModel) => {
    message.loading({ content: 'Changing Password...', key: 'changePassword' });
    const response = await axios.patch(`${API}/users/password`, pswdData, axiosConfig());
    message.destroy('changePassword');
    return response
};