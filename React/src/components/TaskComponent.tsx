import useMessage from "antd/es/message/useMessage";
import { useEffect, useRef, useState } from "react";
import useSWR from "swr";
import { TaskModel, TaskParamModel } from "../models/TaskModel";
import { getTaskUrl, taskFetcher } from "../services/TaskService";
import { Button, Col, Form, Row, Table } from "react-bootstrap";
import { message } from "antd";
import { PaginationComponent } from "./PaginationComponent";
import { useNavigate, useParams } from "react-router-dom";
import { TaskDetailComponent } from "./TaskDetailComponent";

const headers = [{ name: "ID", isCurrentlySorted: false },
{ name: "Summary", isCurrentlySorted: false },
{ name: "Description", isCurrentlySorted: false },
{ name: "Status", isCurrentlySorted: false },
{ name: "Priority", isCurrentlySorted: false },
{ name: "Created At", isCurrentlySorted: false },
{ name: "User ID", isCurrentlySorted: false },
{ name: "Actions", isCurrentlySorted: false }
]

export const TaskComponent = () => {
    const navigate = useNavigate()
    const [messageApi, contextHolder] = useMessage();
    const [collapse, setCollapse] = useState(true)
    const { id } = useParams();
    const [show, setShow] = useState(false);
    const modalData = useRef<string | undefined>(id ? id : undefined)
    const handleClose = () => { setShow(false); navigate("/task") };
    const handleShow = () => setShow(true);
    useEffect(() => {
        if (id) {
            handleShow()
        }
    }, [id])
    const [param, setParam] = useState<TaskParamModel>({
        id: "",
        user_id: "",
        summary: "",
        description: "",
        created_from: "",
        created_to: "",
        all: false,
        page: 1,
        size: 15
    });
    const handleSetParam = (name: string, value: string) => {
        setParam((p) => ({ ...p, [name]: value }));

        if (name !== "page") {
            setParam((p) => ({ ...p, page: 0 }));
        }
    };
    const { data, isLoading, mutate } = useSWR(getTaskUrl(param), taskFetcher, {
        onError: () => {
            messageApi.error("Fail to Load Tasks")
            message.destroy("loadingTasks")
        },
        shouldRetryOnError: false,
        // revalidateOnFocus: false,
    })

    const task: TaskModel[] = []
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
            task.push(t)
        })
    }
    function handleRowClick(data: TaskModel) {
        modalData.current = data.id
        navigate("/task/" + data.id)
    }

    return (
        <div style={{ paddingTop: "10px" }}>
            {contextHolder}
            <Row>
                <Col>
                    <Button onClick={() => { setCollapse(!collapse) }}>{collapse ? "Expand" : "Collapse"}</Button>
                </Col>
                <Col>
                    <Form>
                        <Form.Select name="all" onChange={(e) => { handleSetParam("all", e.target.value) }}>
                            <option value={"false"}>My Task</option>
                            <option value="true">All Tasks</option>
                        </Form.Select>
                    </Form>
                </Col>
            </Row>
            {isLoading ?
                <div>
                    loading
                </div>
                :
                <>
                    {
                        data ? <>
                            <Table hover striped responsive style={{ width: "100%", maxWidth: "100%" }}>
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
                                    {task?.map((data: TaskModel, index) => (
                                        <tr key={index} onClick={() => {
                                            handleRowClick(data)
                                        }}>
                                            {
                                                Object.entries(data).map(([key, value], idx) => (
                                                    <td key={key + '' + idx} className={'text-truncate ' + (collapse ? "collapsed-td" : "")}>
                                                        {value?.toString() || '\u200B'}
                                                    </td>
                                                )
                                                )
                                            }
                                        </tr>
                                    ))}
                                </tbody>
                            </Table>
                            <PaginationComponent currentPage={data.page} totalPage={data.pages} perPage={data.size} setParamsFunction={handleSetParam} fixPageSize={false} containerRef={undefined}></PaginationComponent>
                        </>
                            :
                            ""
                    }
                </>
            }
            <TaskDetailComponent show={show} handleClose={handleClose} id={modalData.current} mutate = {mutate} />
        </div >
    );
}