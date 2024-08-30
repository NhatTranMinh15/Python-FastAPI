import { message } from "antd";
import { FormEvent, MutableRefObject, useState } from "react";
import { Button, Col, Container, Form, OverlayTrigger, Pagination, Popover, Row } from "react-bootstrap";

type Props = {
    currentPage: number;
    totalPage: number;
    perPage: number
    setParamsFunction: any
    fixPageSize: boolean
    containerRef: MutableRefObject<HTMLDivElement | undefined> | undefined
}
export const PaginationComponent = ({ currentPage, totalPage, setParamsFunction, perPage, fixPageSize, containerRef }: Props) => {
    const isFirstPage = currentPage === 1;
    const isLastPage = currentPage === totalPage;
    const [customPage, setCustomPage] = useState(currentPage);

    const handlePageChange = (page: number) => {
        if (page === currentPage) {
            return
        }
        setParamsFunction("page", page)
    };

    function handlePerPageChange(e: string) {
        if (Number.parseInt(e) <= 0) {
            message.warning("Please choose another value")
            return
        }
        setParamsFunction("size", e)
    }

    function handleCustomPageSubmit(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        // redundant
        if (customPage > totalPage || customPage < 1) {
            message.warning("Please choose another value")
            return
        }
        handlePageChange(customPage);
    }

    const popover = (
        <Popover id="popover-basic" style={{ maxWidth: "200px" }}>
            <Popover.Header style={{ textAlign: "center" }}>Choose Page</Popover.Header>
            <Popover.Body>
                <Form onSubmit={(e) => handleCustomPageSubmit(e)}>
                    <Row>
                        <Col sm={7}>
                            <Form.Control type="number" min={1} max={totalPage} onChange={(e) => { setCustomPage(Number.parseInt(e.target.value)); }}></Form.Control>
                        </Col>
                        <Col sm={5}>
                            <Button type="submit">Go</Button>
                        </Col>
                    </Row>
                </Form>
            </Popover.Body>
        </Popover>
    );

    const renderPageItems = () => {
        const items = [];
        if (totalPage <= 5) {
            for (let i = 1; i <= totalPage; i++) {
                items.push(
                    <Pagination.Item key={i} active={i === currentPage} onClick={() => handlePageChange(i)}> {i} </Pagination.Item>
                );
            }
        }
        else {
            if (currentPage <= 3) {
                for (let i = 1; i <= 5; i++) {
                    items.push(
                        <Pagination.Item key={i} active={i === currentPage} onClick={() => handlePageChange(i)}> {i} </Pagination.Item>
                    );
                }
                items.push(
                    <OverlayTrigger key={"rightEllipsisOverlay"} trigger="click" placement="top" overlay={popover} container={containerRef?.current}>
                        <Pagination.Ellipsis key="rightEllipsis" />
                    </OverlayTrigger>
                )
            }
            else if (totalPage - currentPage <= 2) {
                items.push(
                    <OverlayTrigger key={"leftEllipsisOverlay"} trigger="click" placement="top" overlay={popover} container={containerRef?.current}>
                        <Pagination.Ellipsis key="leftEllipsis" />
                    </OverlayTrigger>
                )
                for (let i = totalPage - 5; i <= totalPage; i++) {
                    items.push(
                        <Pagination.Item key={i} active={i === currentPage} onClick={() => handlePageChange(i)}> {i} </Pagination.Item>
                    );
                }
            }
            else {
                items.push(
                    <OverlayTrigger key={"leftEllipsisOverlay"} delay={{ show: 100, hide: 0 }} trigger="click" placement="top" overlay={popover} rootClose={true} container={containerRef?.current}>
                        <Pagination.Ellipsis key="leftEllipsis" id="leftEllipsis" />
                    </OverlayTrigger>
                )
                for (let i = currentPage - 2; i <= currentPage + 2; i++) {
                    items.push(
                        <Pagination.Item key={i} active={i === currentPage} onClick={() => handlePageChange(i)}> {i} </Pagination.Item>
                    );
                }
                items.push(
                    <OverlayTrigger key={"rightEllipsisOverlay"} delay={{ show: 100, hide: 0 }} trigger="click" placement="top" overlay={popover} rootClose={true} container={containerRef?.current}>
                        <Pagination.Ellipsis key="rightEllipsis" id="rightEllipsis" />
                    </OverlayTrigger>
                )
            }
        }
        return items;
    };

    return (
        <Container>
            <Row className="justify-content-end gy-4 py-4">
                <Col sm={2} style={{ width: "fit-content" }}>
                    {fixPageSize ? "" :
                        <div className="me-5" style={{ maxWidth: "100%", minWidth: "50px", width: "fit-content", textAlign: "left" }}>
                            <Form.Group as={Row} className="" controlId="location">
                                <Form.Select name="location" defaultValue={perPage} style={{ width: "100%" }} onChange={(e) => { handlePerPageChange(e.target.value) }}>
                                    <option value="15" >15 / page</option>
                                    <option value="30" >30 / page</option>
                                    <option value="50" >50 / page</option>
                                    <option value="100" >100 / page</option>
                                </Form.Select>
                            </Form.Group>
                        </div>
                    }
                </Col>
                <Col sm={4} style={{ width: "fit-content" }}>
                    <Pagination className="justify-content-end">

                        <Pagination.First disabled={isFirstPage || totalPage === 0} onClick={() => handlePageChange(1)}>First</Pagination.First>
                        <Pagination.Prev disabled={isFirstPage || totalPage === 0} onClick={() => handlePageChange(currentPage - 1)}>Previous</Pagination.Prev>

                        {renderPageItems()}

                        <Pagination.Next disabled={isLastPage || totalPage === 0} onClick={() => handlePageChange(currentPage + 1)}>Next</Pagination.Next>
                        <Pagination.Last disabled={isLastPage || totalPage === 0} onClick={() => handlePageChange(totalPage)}>Last</Pagination.Last>
                    </Pagination>
                </Col>
            </Row>
        </Container>
    );
}
