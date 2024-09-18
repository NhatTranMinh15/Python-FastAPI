import useSWR from "swr";
import { UserModel } from "../../models/UserModel";
import { getUserUrlWithParam, userFetcher } from "../../services/UserService";
import useMessage from "antd/es/message/useMessage";
import { PaginationComponent } from "../commons/Pagination";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Badge, Button } from "flowbite-react";
import { message } from "antd";
import Loading from "../commons/Loading";


const headers = [
  { name: "ID", value: "id", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  { name: "Email", value: "email", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  { name: "Username", value: "username", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  { name: "First Name", value: "first_name", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  { name: "Last Name", value: "last_name", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  { name: "Is Admin", value: "is_admin", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  { name: "Company ID", value: "company_id", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
  { name: "Created At", value: "created_at", isCurrentlySorted: false, colStyle: {}, hiddenOnSmall: false },
]
const maxColLength = headers.length

export const UserComponent = () => {
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

  const { data, isLoading } = useSWR(getUserUrlWithParam("?" + searchParams.toString()), userFetcher, {
    onError: (error) => {
      if (error.status === 401 || error.status === 403) {
        return navigate('/login')
      }
      messageApi.error("Fail to Load User")
      message.destroy('loadingUsers')
    },
    shouldRetryOnError: false,
    revalidateOnFocus: false,
  })

  let users: UserModel[] = []
  if (data) {
    users = data.items
  }

  function handleRowClick(data: UserModel) {
    navigate(data.id)
  }

  function switchValue(user: UserModel, value: string) {
    switch (value) {
      case "is_admin":
        return <Badge className={"justify-center w-fit  " + (user.is_admin ? "outline-green" : "outline-red")}>{user.is_admin ? "True" : "False"}</Badge>
      case "company_id":
        return user.company_id || "None"
      default:
        return user[value]
    }
  }

  return (
    <>
      {contextHolder}
      <div className="flex flex-row">
        <div className="basis-1/2 p-2">

        </div>
        <div className="basis-1/2 p-2">
          <Button color={"green"} className="border border-green-500" onClick={() => { navigate("create") }}>Create New User</Button>
        </div>

      </div>
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
            {users.map((user: UserModel) => (
              <tr key={user.id} className="table-row hoverable" onClick={() => { handleRowClick(user) }}>
                {
                  headers.map((header) => (
                    <td key={header.value + " " + user.id} className={"truncate " + (header.hiddenOnSmall ? "hidden md:table-cell " : " ")} style={{ maxWidth: `${100 / maxColLength - 1}vw` }}>
                      {switchValue(user, header.value)}
                    </td>
                  ))
                }
              </tr>
            ))
            }
          </tbody>
        </table>
        <PaginationComponent currentPage={data ? data.page : 1} totalPage={data ? data.pages : 1} perPage={data ? data.size : 0} setParamsFunction={handleSetParam} fixPageSize={false} containerRef={undefined}></PaginationComponent>
      </div>
      <Loading view={isLoading} message={"Loading Users ..."}></Loading>
    </>
  );
}