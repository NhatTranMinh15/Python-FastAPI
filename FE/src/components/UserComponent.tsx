import { useState } from "react";
import { Table } from "react-bootstrap";
import useSWR from "swr";
import { UserModel, UserParamModel } from "../models/UserModel";
import { getUserUrl, userFetcher } from "../service/UserService";
import useMessage from "antd/es/message/useMessage";


const headers = [{ name: "ID", isCurrentlySorted: false }, { name: "Email", isCurrentlySorted: false }, { name: "Username", isCurrentlySorted: false }, { name: "First Name", isCurrentlySorted: false }, { name: "Last Name", isCurrentlySorted: false }, { name: "Created At", isCurrentlySorted: false }, { name: "Is Admin", isCurrentlySorted: false }, { name: "Company ID", isCurrentlySorted: false }, { name: "Actions", isCurrentlySorted: false }]
export const UserComponent = () => {
    const [messageApi, contextHolder] = useMessage();

    const [param] = useState<UserParamModel>({
        email: undefined,
        first_name: undefined,
        username: undefined,
        last_name: undefined,
        page: 1,
        size: 15
    });
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
        <div>
            {contextHolder}
            {isLoading ?
                <div>
                    loading

                </div>
                :
                <Table hover responsive style={{ width: "auto", maxWidth: "100%" }}>
                    <thead>
                        <tr>
                            {headers?.map((h) => (
                                <th key={h.name} className={"header-border"} style={{ overflow: "hidden" }}>
                                    {h.name.length > 0 ?
                                        <div className={'table-header ' + (h.isCurrentlySorted ? "sorting-header" : "")}>
                                            <div>
                                                {h.name}
                                            </div>
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
                                        <td key={key + '' + idx} className='text-truncate' style={{textOverflow:"hidden"}}>
                                            {value?.toString() || '\u200B'}
                                        </td>
                                    )
                                    )
                                }
                                <td className='last-cell '>
                                    BUTTON
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            }
        </div>
    );
}