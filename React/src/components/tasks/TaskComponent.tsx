import useMessage from "antd/es/message/useMessage";
import useSWR from "swr";
import { PriorityColor, StatusColor, TaskModel } from "../../models/TaskModel";
import { getTaskUrlWithParam, taskFetcher } from "../../services/TaskService";
import { message } from "antd";
import { Outlet, useNavigate, useSearchParams } from "react-router-dom";
import { PaginationComponent } from "../commons/Pagination";
import { Badge, Button } from "flowbite-react";

const headers = [
    { name: "ID", value: "id", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
    { name: "Summary", value: "summary", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
    // { name: "Description", value: "description", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: true },
    { name: "Status", value: "status", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
    { name: "Priority", value: "priority", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: true },
    { name: "Created At", value: "created_at", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: true },
    // { name: "User ID", value: "user_id", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: true },
]

const maxColLength = headers.length

export const TaskComponent = () => {
    const navigate = useNavigate()
    const [messageApi, contextHolder] = useMessage();
    const [searchParams, setSearchParams] = useSearchParams("all=false&page=1&size=15");

    const handleSetParam = (name: string, value: string) => {
        searchParams.set(name, value)
        if (name !== "page") {
            searchParams.set("page", "1")
        }
        setSearchParams(searchParams)
    };

    const { data, isLoading } = useSWR(getTaskUrlWithParam("?" + searchParams.toString()), taskFetcher, {
        onError: (err) => {
            if (err.status === 401 || err.status === 403) {
                messageApi.error("Your session expired. Please login again").then(() => {
                    // navigate("/login")
                })
                return
            }
            messageApi.error("Fail to Load Tasks")
            message.destroy("loadingTasks")
        },
        shouldRetryOnError: false,
        revalidateOnFocus: false,
    })

    const tasks: TaskModel[] = []
    if (data) {
        data.items.map((ts) => {
            const t: TaskModel = {
                id: ts.id,
                summary: ts.summary,
                description: ts.description,
                status: ts.status,
                priority: ts.priority,
                created_at: ts.created_at,
                user_id: ts.user?.id
            }
            tasks.push(t)
        })
    }
    function handleRowClick(data: TaskModel) {
        navigate(data.id)
    }

    return (
        <>
            {contextHolder}
            <div className="flex flex-row">
                <div className="basis-1/4 p-2">
                    <select name="all" defaultValue={searchParams.get("all") || "false"} className="w-full" onChange={(e) => { handleSetParam("all", e.target.value) }}>
                        <option value={"false"}>My Task</option>
                        <option value="true">All Tasks</option>
                    </select>
                </div>
                <div className="basis-1/4 p-2">
                    <Button color={"green"} className="border border-green-500" onClick={() => { navigate("create") }}>Create New Task</Button>
                </div>
            </div>
            {isLoading ?
                <div>
                    loading
                </div>
                :
                <>
                    {
                        data ?
                            <div className="flex flex-col w-full mt-4">
                                <table className="border-collapse table-auto">
                                    <thead className="table-header-group">
                                        <tr className="table-row">
                                            {headers?.map((h) => (
                                                <th key={h.name} className={"table-cell header-border "} style={{ overflow: "hidden" }}>
                                                    {h.name.length > 0 ?
                                                        <div className={'table-header ' + (h.isCurrentlySorted ? "sorting-header" : "")}>
                                                            {h.name}
                                                        </div>
                                                        : '\u200B'
                                                    }
                                                </th>
                                            ))}
                                        </tr>
                                    </thead>
                                    <tbody className="table-row-group divide-y max-w-full">
                                        {tasks?.map((task: TaskModel) => (
                                            <tr key={task.id} className="table-row hoverable" onClick={() => { handleRowClick(task) }}>
                                                {headers.map((header) => {
                                                    switch (header.value) {
                                                        case "status":
                                                            return (
                                                                <td key={header.value + " " + task.id}>
                                                                    <Badge className={"justify-center w-fit " + StatusColor[task[header.value] as keyof typeof StatusColor]}>{task[header.value]}</Badge>
                                                                </td>
                                                            )
                                                        case "priority":
                                                            return (
                                                                <td key={header.value + " " + task.id}>
                                                                    <Badge className={"justify-center w-fit " + PriorityColor[task[header.value] as keyof typeof PriorityColor]}>{task[header.value]}</Badge>
                                                                </td>
                                                            )
                                                        default:
                                                            return (<td key={header.value + " " + task.id} className={"truncate " + (header.hiddenOnSmall ? "hidden md:table-cell " : " ")} style={{ maxWidth: `${100 / maxColLength - 1}vw` }}>
                                                                {task[header.value]}
                                                            </td>)
                                                    }
                                                })}
                                            </tr>
                                        ))
                                        }
                                    </tbody>
                                </table>
                                <PaginationComponent currentPage={data ? data.page : 1} totalPage={data ? data.pages : 1} perPage={data ? data.size : 1} setParamsFunction={handleSetParam} fixPageSize={false} containerRef={undefined}></PaginationComponent>
                            </div>
                            :
                            ""
                    }
                </>
            }
        </>
    );
}