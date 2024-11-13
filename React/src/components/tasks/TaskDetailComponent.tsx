import { message } from "antd";
import useMessage from "antd/es/message/useMessage";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import { CreateTaskModel, Priority, PriorityColor, Status, StatusColor, TaskModel, TaskModelShort } from "../../models/TaskModel";
import { deleteTask, getOneTask, getOneTaskUrl, updateTask } from "../../services/TaskService";
import { useFormik } from "formik";
import useSWR from "swr";

export const TaskDetailComponent = () => {
    // console.log("Render TaskDetailComponent");

    const navigate = useNavigate()
    const [messageApi, contextHolder] = useMessage();
    const { id } = useParams();

    const { data: task } = useSWR<TaskModel>(id ? getOneTaskUrl(id) : null, getOneTask, {
        onError(err) {
            if (err.status === 401 || err.status === 403) {
                message.error("Your session expired. Please login again").then(() => {
                    navigate("/login")
                })
            }
            message.destroy("loadingTask")
        },
        revalidateOnFocus: false,
        shouldRetryOnError: false,
    })

    const formik = useFormik<TaskModelShort>({
        initialValues: {
            id: task?.id || "",
            summary: task?.summary || "",
            description: task?.description || "",
            status: task?.status || Status.OPEN,
            priority: task?.priority || Priority.MEDIUM,
            created_at: task?.created_at.slice(0, 23) || "",
            user_id: task?.user?.id || ""
        },
        enableReinitialize: true,

        // validationSchema: validationSchema,
        onSubmit: async (values) => {
            const body: CreateTaskModel = {
                summary: values.summary,
                description: values.description,
                status: Status[values.status as keyof typeof Status],
                priority: Priority[values.priority as keyof typeof Priority],
                user_id: undefined
            };
            messageApi.loading({ content: 'Updating Task...', key: 'updateTask', duration: 0 });
            await updateTask(values.id, false, body)
                .then((res) => {
                    if (res.status == 200) {
                        // const data: TaskModel = res.data;
                    }
                })
                .catch((err) => {
                    console.log(err);
                }).finally(() => {
                    messageApi.destroy("updateTask")
                });
        }
    });


    const { dirty, getFieldProps } = formik

    async function handledeleteTask(id: string) {
        const userConfirmed = window.confirm("Are you sure you want to delete this task?");
        if (userConfirmed) {
            messageApi.loading({ content: 'Deleting Task...', key: 'deleteTask', duration: 0 });
            await deleteTask(id).then(() => {
                navigate("/tasks")
                message.success("Delete Task Successfully");
            }).catch(() => { messageApi.error("Failed to Delete Task"); }).finally(() => {
                messageApi.destroy('deleteTask')
            })
        }
    }
    if (!id) {
        return <Navigate to={"/tasks"} />
    }
    return task &&
        <form className="task-detail-view flex flex-col m-4 p-4 gap-4" onSubmit={formik.handleSubmit}>
            {contextHolder}
            <div className="flex flex-col md:flex-row gap-5 items-center justify-between">
                <div className="w-full">
                    <input className="input w-full text-2xl" {...getFieldProps("summary")} />
                </div>
                <div className="flex flex-col sm:flex-row gap-4">
                    <select  {...getFieldProps("status")} name="status" id="status" className={"select-green w-full " + StatusColor[formik.values.status as keyof typeof StatusColor]}>
                        {Object.keys(Status).map((status) => {
                            return (
                                <option key={status} className="option-green" value={status}>{status}</option>
                            )
                        })}
                    </select>
                    <select {...getFieldProps("priority")} name="priority" id="priority" className={"select-green w-full " + PriorityColor[formik.values.priority as keyof typeof PriorityColor || task.priority as keyof typeof PriorityColor]}>
                        {Object.keys(Priority).map((priority) => {
                            return (
                                <option key={priority} className="option-green" value={priority}>{priority}</option>
                            )
                        })}
                    </select>
                </div>
            </div>

            <div className="main-content h-full">
                <h2 className="text-xl font-bold mb-2">Description:</h2>
                <textarea {...getFieldProps("description")} className="input w-full h-full min-h-16 min-w-16 max-h-60 rounded-md overflow-visible" />
            </div>
            <div className="metadata">
                <div className="mb-2">
                    <h2 className="text-xl font-bold inline-block mr-4">
                        Assignee:</h2>
                    {task.user ?
                        <Link to={"/user/" + task.user?.id} className="user-link ">
                            {task.user.first_name + " " + task.user.last_name}
                        </Link>
                        : "None"
                    }
                </div>
                <div>
                    <h2 className="text-xl font-bold inline-block mr-4">Create Date:</h2>
                    <input type="datetime-local" className="input max-w-30ch rounded" {...getFieldProps("created_at")} value={formik.values.created_at || task.created_at.slice(0, 23)}></input>
                </div>
            </div>
            <div className="actions flex flex-row gap-5">
                <button className="button button-yellow" type="submit" disabled={!dirty}>Change</button>
                <button className="button button-red" onClick={(e) => { e.preventDefault(); handledeleteTask(task.id) }}>Delete</button>
            </div>
        </form>
}