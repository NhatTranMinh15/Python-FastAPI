import axios from "axios";
import { PageResponseModel } from "../models/PageModel";
import { axiosConfig, URL } from "../utils/Config";
import { CreateTaskModel, TaskModel, TaskParamModel } from "../models/TaskModel";

const taskURL = URL + "/tasks"
export const getTaskUrl = (params: TaskParamModel) => taskURL + buildParam(params);
export const getTaskUrlWithParam = (params: string) => taskURL + params;
export const getOneTaskUrl = (id: string) => { return taskURL + "/" + id; };

export const getOneTask = async (url: string) => {
    const response = await axios.get(url, axiosConfig())
    const data: TaskModel = response.data;
    return data
}
export const taskFetcher = async (url: string) => {
    const response = await axios.get(url, axiosConfig())
    const data: PageResponseModel<TaskModel> = response.data;
    return data;
}
export const createTask = async (data: CreateTaskModel) => {
    const response = await axios.post(taskURL, data, axiosConfig());
    return response
}
export const updateTask = async (id: string, remove_user: boolean = false, data: CreateTaskModel) => {
    const url = `${taskURL}/${id}?remove_user=${remove_user}`
    const response = await axios.put(url, data, axiosConfig());
    return response
}
export function buildParam(params: TaskParamModel) {
    const param = "?"
        + (params.id ? "id=" + params.id + "&" : "")
        + (params.summary ? "summary=" + params.summary + "&" : "")
        + (params.description ? "description=" + params.description + "&" : "")
        + (params.user_id ? "user_id=" + params.user_id + "&" : "")
        + (params.created_from ? "created_from=" + params.created_from + "&" : "")
        + (params.created_to ? "created_to=" + params.created_to + "&" : "")
        + (params.all ? "all=" + params.all + "&" : "all=false&")
        + (params.page ? "page=" + params.page + "&" : "page=1&")
        + (params.size ? "size=" + params.size : "size=15&")
    return param;
}

export const deleteTask = async (id: string) => axios.delete(taskURL + "/" + id, axiosConfig())