import { message } from "antd";
import useMessage from "antd/es/message/useMessage";
import { Button, Col, Container, Modal, Row } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import useSWR from "swr";
import { PriorityColor, StatusMap } from "../models/TaskModel";
import { deleteTask, getOneTask, getOneTaskUrl } from "../services/TaskService";
type Props = {
    show: boolean
    handleClose: any
    id: string | undefined
    mutate: any
}
export const TaskDetailComponent = ({ show, handleClose, id, mutate }: Props) => {
    const navigate = useNavigate()
    const [messageApi] = useMessage();

    const { data: task } = useSWR(id ? getOneTaskUrl(id) : null, getOneTask, {
        onError() {
            handleClose()
            message.destroy("loadingTask")
        },
        revalidateOnFocus: false,
        shouldRetryOnError: false,

    })
    async function handledeleteTask(id: string) {
        messageApi.loading({ content: 'Deleting Task...', key: 'deleteTask', duration: 0 });
        await deleteTask(id).then(() => {
            handleClose()
            message.success("Delete Task Successfully");
            mutate()
            navigate("/task")
        })
            .catch(() => {
                messageApi.error("Failed to Delete Task");
            })
        messageApi.destroy('deleteTask')
    }
    return (
        <Modal show={show}
            onHide={handleClose}
            centered backdrop={true}
        >
            <Modal.Body>
                {task ? <Container className="task-detail-view" style={{ marginTop: "10px" }}>
                    <div>
                        <Row>
                            <h1>{task.summary}</h1>
                        </Row>
                        <Row>
                            <Col sm={"auto"} className={"ms-3 p-2 ps-3 pe-3 rounded " + StatusMap[task.status]}>
                                {task.status}
                            </Col>

                            <Col sm={"auto"} className={"ms-3 p-2 ps-3 pe-3 rounded " + PriorityColor[task.priority as keyof typeof PriorityColor]}>
                                {task.priority}
                            </Col>
                        </Row>
                    </div>
                    <div className="main-content">
                        <div className="description">
                            <h2>Description</h2>
                            <p>{task.description}</p>
                        </div>
                        {/* <div className="subtasks">
                        <h2>Subtasks</h2>
                        <ul>
                        <li><input type="checkbox" /> Subtask 1</li>
                        <li><input type="checkbox" /> Subtask 2</li>
                        </ul>
                        </div> */}
                        {/* <div className="attachments">
                        <h2>Attachments</h2>
                        <ul>
                        <li><a href="#">File 1</a></li>
                        <li><a href="#">File 2</a></li>
                        </ul>
                        </div>
                        <div className="comments">
                        <h2>Comments</h2>
                        <div className="comment">
                        <p><strong>User 1:</strong> Comment text...</p>
                        </div>
                        <div className="comment">
                        <p><strong>User 2:</strong> Another comment...</p>
                        </div>
                        </div> */}
                    </div>
                    <div className="metadata">
                        <strong>Assignee: <Link to={"/user/" + task.user?.id}>{task.user?.first_name + " " + task.user?.last_name}</Link></strong>
                        <p><strong>Create Date:</strong> {task.created_at.split("T")[0]}</p>
                        {/* <p><strong>Created By:</strong> Jane Smith on 2024-08-25</p> */}
                        {/* <p><strong>Tags:</strong> Tag1, Tag2</p> */}
                    </div>
                    <div className="actions">
                        <Button variant="warning">Edit</Button>
                        <Button variant="danger" onClick={() => { handledeleteTask(task.id) }}>Delete</Button>
                        {/* <button>Mark as Complete</button> */}
                        {/* <button>Add Subtask</button> */}
                        {/* <button>Add Comment</button> */}
                    </div>
                    {/* <div className="activity-log">
                <h2>Activity Log</h2>
                <ul>
                <li>2024-08-25: Task created by Jane Smith</li>
                <li>2024-08-26: Status changed to In Progress by John Doe</li>
                </ul>
                </div> */}
                </Container>
                    : ""
                }
            </Modal.Body>
        </Modal>
    );
}