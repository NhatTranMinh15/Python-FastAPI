import { useRef, useState } from "react";
import { Button, Table } from "react-bootstrap";
import useSWR from "swr";
import { UserModel, UserParamModel } from "../models/UserModel";
import { getUserUrl, userFetcher } from "../services/UserService";
import useMessage from "antd/es/message/useMessage";
import { PaginationComponent } from "./PaginationComponent";


const headers = [{ name: "ID", isCurrentlySorted: false }, { name: "Email", isCurrentlySorted: false }, { name: "Username", isCurrentlySorted: false }, { name: "First Name", isCurrentlySorted: false }, { name: "Last Name", isCurrentlySorted: false }, { name: "Created At", isCurrentlySorted: false }, { name: "Is Admin", isCurrentlySorted: false }, { name: "Company ID", isCurrentlySorted: false }, { name: "Actions", isCurrentlySorted: false }]
export const UserComponent = () => {
    const [collapse, setCollapse] = useState(true)
    const [messageApi, contextHolder] = useMessage();
    const c = useRef()
    const [param, setParam] = useState<UserParamModel>({
        email: undefined,
        first_name: undefined,
        username: undefined,
        last_name: undefined,
        page: 1,
        size: 15
    });
    const handleSetParam = (name: string, value: string) => {
        console.log(name, value);

        setParam((p) => ({ ...p, [name]: value }));

        if (name !== "page") {
            setParam((p) => ({ ...p, page: 0 }));
        }
    };
    const { data, isLoading } = useSWR(getUserUrl(param), userFetcher, {
        onError: () => {
            messageApi.error("Fail to Load User")
            messageApi.destroy('loadingUsers')
        },
        shouldRetryOnError: false,
        revalidateOnFocus: false,
    })

    let user: UserModel[] = []
    if (data) {
        user = data.items
    }

    return (
        <div style={{ paddingTop: "10px" }}>
            {contextHolder}
            <Button onClick={() => { setCollapse(!collapse) }}>{collapse ? "Expand" : "Collapse"}</Button>
            {isLoading ?
                <div>
                    loading

                </div>
                :
                <>
                    {
                        data ?
                            <>
                                <Table hover responsive style={{ width: "100%", maxWidth: "100%" }}>
                                    <thead>
                                        <tr>
                                            {headers?.map((h) => (
                                                <th key={h.name} className={"header-border text-truncate"} style={{ overflow: "hidden" }}>
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
                                    <tbody style={{ maxWidth: "100%" }}>
                                        {user?.map((data: UserModel, index) => (
                                            <tr key={index}>
                                                {
                                                    Object.entries(data).map(([key, value], idx) => (
                                                        <td key={key + '' + idx} className={'text-truncate ' + (collapse ? "collapsed-td" : "")}>
                                                            {value?.toString() || '\u200B'}
                                                        </td>
                                                    )
                                                    )
                                                }
                                                <td className='last-cell'>
                                                    BUTTON
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </Table>
                                <PaginationComponent currentPage={data.page} totalPage={data.pages} perPage={data.size} setParamsFunction={handleSetParam} fixPageSize={false} containerRef={c}></PaginationComponent>
                            </> : ""
                    }
                </>
            }
        </div>
    );
}