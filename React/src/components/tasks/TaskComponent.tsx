import useMessage from "antd/es/message/useMessage";
import useSWR from "swr";
import { PriorityColor, StatusColor, TaskModel } from "../../models/TaskModel";
import { getTaskUrlWithParam, taskFetcher } from "../../services/TaskService";
import { message } from "antd";
import { useNavigate, useSearchParams } from "react-router-dom";
import { PaginationComponent } from "../commons/Pagination";
import Loading from "../commons/Loading";

const headers = [
  { name: "ID", value: "id", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  { name: "Summary", value: "summary", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  // { name: "Description", value: "description", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: true },
  { name: "Status", value: "status", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  { name: "Priority", value: "priority", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  // { name: "Created At", value: "created_at", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: true },
  { name: "Asignee", value: "user", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: true },
]

const maxColLength = headers.length

export const TaskComponent = () => {
  // console.log("Render TaskComponent");

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

  const { data, isLoading } = useSWR(getTaskUrlWithParam(`?${searchParams.toString()}`), taskFetcher, {
    onError: (err) => {
      if (err.status === 401 || err.status === 403) {
        messageApi.error("Your session expired. Please login again").then(() => {
          navigate("/login")
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
    tasks.push(...data.items)
  }

  function handleRowClick(data: TaskModel) {
    if (!window.getSelection()?.toString()) {
      navigate(data.id)
    }
  }
  return (
    <>
      {contextHolder}
      <div className="flex flex-row">
        <div className="basis-1/4 p-2">
          <select name="select-all-tasks" defaultValue={searchParams.get("all") || "false"} className="w-full select-green" onChange={(e) => { handleSetParam("all", e.target.value) }}>
            <option value={"false"} className="">My Task</option>
            <option value="true" className="">All Tasks</option>
          </select>
        </div>
        <div className="basis-1/4 p-2">
          <button className="button button-green" onClick={() => { navigate("create") }}>Create New Task</button>
        </div>
      </div>
      {isLoading ?
        <div>
          <Loading view={isLoading} message={"Loading Tasks ..."} />
        </div>
        :
        <>
          {
            data &&
            <div className="flex flex-col w-full mt-4">
              <table className="border-collapse table-auto">
                <thead className="table-header-group">
                  <tr className="table-header-row">
                    {headers?.map((h) => (
                      <th key={h.name} className={"header-border " + (h.hiddenOnSmall ? "hidden md:table-cell" : "")} style={{ overflow: "hidden" }}>
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
                    <tr key={task.id} className="table-row hoverable-row" onClick={(e) => { e.stopPropagation(); handleRowClick(task) }}>
                      {/* {headers.map((header) => {
                        switch (header.value) {
                          case "status":
                            return (
                              <td key={header.value + " " + task.id}>
                                <span className={"badge " + StatusColor[task[header.value] as keyof typeof StatusColor]}>{task[header.value]}</span>
                              </td>
                            )
                          case "priority":
                            return (
                              <td key={header.value + " " + task.id}>
                                <span className={"badge " + PriorityColor[task[header.value] as keyof typeof PriorityColor]}>{task[header.value]}</span>
                              </td>
                            )
                          case "user":
                            return (
                              <td key={header.value + " " + task.id}>
                                {task.user ? `${task.user.first_name} ${task.user.last_name}` : "None"}
                              </td>
                            )
                          default:
                            return (<td key={header.value + " " + task.id} className={"truncate " + (header.hiddenOnSmall ? "hidden md:table-cell " : " ")} style={{ maxWidth: `${100 / maxColLength - 1}vw` }}>
                              {task[header.value]?.toString() || ""}
                            </td>)
                        }
                      })} */}
                      {
                        headers.map((header) => {
                          return (
                            <td key={header.value + " " + task.id} className={"truncate " + (header.hiddenOnSmall ? "hidden md:table-cell " : " ")} style={{ maxWidth: `${100 / maxColLength - 1}vw` }}>
                              {(() => {
                                switch (header.value) {
                                  case "status":
                                    return <span className={"badge " + StatusColor[task[header.value] as keyof typeof StatusColor]}>{task[header.value]}</span>
                                  case "priority":
                                    return <span className={"badge " + PriorityColor[task[header.value] as keyof typeof PriorityColor]}>{task[header.value]}</span>
                                  case "user":
                                    return task.user ? `${task.user.first_name} ${task.user.last_name}` : "None";
                                  default:
                                    // Add your default case code here
                                    return task[header.value]?.toString() || "";
                                }
                              })()}
                            </td>
                          )
                        })
                      }
                    </tr>
                  ))
                  }
                </tbody>
              </table>
              <PaginationComponent currentPage={data ? data.page : 1} totalPage={data ? data.pages : 1} perPage={data ? data.size : 1} setParamsFunction={handleSetParam} fixPageSize={false} containerRef={undefined}></PaginationComponent>
            </div>
          }
        </>
      }
    </>
  );
}