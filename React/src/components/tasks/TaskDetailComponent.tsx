import { message } from "antd";
import useMessage from "antd/es/message/useMessage";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Priority, PriorityColor, Status, StatusColor, TaskResponseModel } from "../../models/TaskModel";
import { deleteTask, getOneTask, getOneTaskUrl } from "../../services/TaskService";
import { Button } from "flowbite-react";
import { useFormik } from "formik";
import useSWRImmutable from "swr/immutable";
type Props = {
    show: boolean
};
export const TaskDetailComponent = ({ show }: Props) => {
    const navigate = useNavigate()
    const [messageApi] = useMessage();
    const { id } = useParams();
    console.log(id);

    const { data: task } = useSWRImmutable<TaskResponseModel>(id ? getOneTaskUrl(id) : null, getOneTask, {
        onError() {
            message.destroy("loadingTask")
        },
        revalidateOnFocus: false,
        shouldRetryOnError: false,
    })

    const formik = useFormik({
        initialValues: {

            id: task?.id || "",
            summary: task?.summary || "",
            description: task?.description || "",
            status: task?.status || "",
            priority: task?.priority || "",
            created_at: task?.created_at.slice(0, 23) || "",
            user_id: task?.user?.id || ""
        },
        enableReinitialize: true,

        // validationSchema: validationSchema,
        onSubmit: async (values) => {
            // const logInData: LogInModel = {
            //     username: values.username,
            //     password: values.password,
            // };
            // setLoading(true);
            // await login(logInData)
            //     .then((res) => {
            //         if (res.status == 200) {
            //             const loginResponse: LogInResponseModel = {
            //                 token_type: res.data.token_type,
            //                 access_token: res.data.access_token
            //             }
            //             sessionStorage.setItem("jwt_token", JSON.stringify(loginResponse))
            //             messageApi.success("Login Successfully", 2);
            //             navigate("/tasks")
            //         }
            //     })
            //     .catch((err) => {
            //         setLoading(false);
            //         if (err.response?.status === 401) {
            //             messageApi.error('Wrong email or password');
            //         }
            //         if (err.response.status == 403) {
            //             messageApi.error('You do not have permission to access this page!');
            //         }
            //     });
        }
    });


    const { dirty, getFieldProps } = formik

    async function handledeleteTask(id: string) {
        messageApi.loading({ content: 'Deleting Task...', key: 'deleteTask', duration: 0 });
        await deleteTask(id).then(() => {
            message.success("Delete Task Successfully");
            navigate("/tasks")
        })
            .catch(() => {
                messageApi.error("Failed to Delete Task");
            })
        messageApi.destroy('deleteTask')
    }

    return id && task ?
        <form className="task-detail-view flex flex-col m-4 p-4 gap-4" onSubmit={formik.submitForm}>
            <div className="flex items-center justify-between">
                <div className="w-full">
                    <input {...getFieldProps("summary")} className="w-11/12 text-2xl text-zinc-500 font-bold inline-block overflow-x-auto" />
                </div>
                <div className="flex flex-row">
                    <select  {...getFieldProps("status")} name="status" id="status" className={"ms-3 p-2 ps-3 pe-3 border rounded " + StatusColor[formik.values.status as keyof typeof StatusColor]}>
                        {Object.keys(Status).map((s) => {
                            return (
                                <option key={s} className="bg-white text-black disabled:bg-slate-200 disabled:cursor-not-allowed" value={s}>{s}</option>
                            )
                        })}
                    </select>
                    <select {...getFieldProps("priority")} name="priority" id="priority" className={"ms-3 p-2 ps-3 pe-3 border rounded " + PriorityColor[formik.values.priority as keyof typeof PriorityColor || task.priority as keyof typeof PriorityColor]}>
                        {Object.keys(Priority).map((p) => {
                            return (
                                <option key={p} className="bg-white text-black disabled:bg-slate-200 disabled:cursor-not-allowed" value={p}>{p}</option>
                            )
                        })}
                    </select>
                </div>
            </div>

            <div className="main-content h-full">
                <h2 className="text-xl font-bold mb-2">Description:</h2>
                <textarea {...getFieldProps("description")} className="w-full h-full min-h-16 min-w-16 max-h-60 rounded-md overflow-visible" />
            </div>
            <div className="metadata">
                <div className="mb-2">
                    <h2 className="text-xl font-bold inline-block mr-2">
                        Assignee: {"  "}</h2>
                    {
                        task.user ?
                            <Link to={"/user/" + task.user?.id} className="user-link ">{task.user.first_name + " " + task.user.last_name}</Link>
                            : "None"
                    }
                </div>
                <div>
                    <h2 className="text-xl font-bold inline-block mr-2">Create Date:</h2>
                    <input type="datetime-local" className="rounded" {...getFieldProps("created_at")} value={formik.values.created_at || task.created_at.slice(0, 23)}></input>
                </div>
            </div>
            <div className="actions flex flex-row gap-5">
                <Button color={"yellow"} disabled={!dirty}>Change</Button>
                <Button color={"red"} onClick={() => { handledeleteTask(task.id) }}>Delete</Button>
            </div>
        </form>
        :
        <></>
}