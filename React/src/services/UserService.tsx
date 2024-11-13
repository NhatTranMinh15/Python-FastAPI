import axios from "axios";
import { PageResponseModel } from "../models/PageModel";
import { UserModel, UserParamModel } from "../models/UserModel";
import { URL, axiosConfig } from "../utils/Config";

const userURL = `${URL}/users`;
export const getUserUrl = (params: UserParamModel) => `${userURL}${buildParam(params)}`;
export const getUserUrlWithParam = (params: string) => `${userURL}${params}`;

export const userFetcher = async (url: string) => {
    await simulateLongApiCall();
    const response = await axios.get(url, axiosConfig())
    const data: PageResponseModel<UserModel> = response.data;
    return data;
}
function buildParam(params: UserParamModel) {
    const param = "?"
        + (params.email ? "email=" + params.email + "&" : "")
        + (params.username ? "username=" + params.username + "&" : "")
        + (params.first_name ? "first_name=" + params.first_name + "&" : "")
        + (params.last_name ? "last_name=" + params.last_name + "&" : "")
        + (params.page ? "page=" + params.page + "&" : "")
        + (params.size ? "size=" + params.size : "")
    return param;
}
const simulateLongApiCall = (): Promise<string> => {
    const duration = Math.floor((Math.random() * 1000) + 1);
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve("URL call completed");
        }, duration);
    });
};