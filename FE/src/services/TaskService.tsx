import { message } from "antd";
import axios from "axios";
import { PageResponseModel } from "../models/PageModel";
import { API, axiosConfig } from "../utils/Config";
import { TaskParamModel, TaskResponseModel } from "../models/TaskModel";


export const getTaskUrl = (params: TaskParamModel) => API + "/tasks" + buildParam(params);
export const getOneTaskUrl = (id: string) => { return API + "/tasks/" + id; };
export const getOneTask = async (url: string) => {
    message.loading({ content: 'Loading Task Detail...', key: 'loadingTask', duration: 0 });
    const response = await axios.get(url, axiosConfig())
    const data: TaskResponseModel = response.data;
    message.destroy('loadingTask')
    return data

}
export const taskFetcher = async (url: string) => {
    message.loading({ content: 'Loading Tasks...', key: 'loadingTasks', duration: 0 });
    const response = await axios.get(url, axiosConfig())
    const data: PageResponseModel<TaskResponseModel> = response.data;
    message.destroy('loadingTasks')
    return data;
}
function buildParam(params: TaskParamModel) {
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

export const deleteTask = async (id: string) => axios.delete(API + "/tasks/" + id, axiosConfig())
