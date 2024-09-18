import { message } from "antd";
import { FormEvent, MutableRefObject, useState } from "react";
import { Popover } from "flowbite-react";

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
    console.log(perPage);

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

    const popover = (key: string) => {
        return (
            <Popover key={key} id="popover-basic" className="max-w-52 border border-black rounded-lg" content={
                <>
                    <div className="bg-gray-200 px-3 py-2 text-center dark:border-gray-600 dark:bg-gray-700">
                        <h3 id="default-popover" className="font-semibold text-gray-900 dark:text-white">
                            Choose Page
                        </h3>
                    </div>
                    <div className="px-3 py-2">
                        <form onSubmit={(e) => handleCustomPageSubmit(e)}>
                            <input className="rounded-xl mr-2" type="number" min={1} max={totalPage} onChange={(e) => { setCustomPage(Number.parseInt(e.target.value)); }}></input>
                            <button className="py-2 px-5 border hover:bg-zinc-300 rounded-xl" type="submit">Go</button>
                        </form>
                    </div>
                </>
            }>
                <button className="pagination-button">...</button>
            </Popover >
        )
    };

    const renderPageItems = () => {
        const items = [];
        if (totalPage <= 5) {
            for (let i = 1; i <= totalPage; i++) {
                items.push(
                    <button className="pagination-button" key={i} disabled={i === currentPage} onClick={() => handlePageChange(i)}> {i} </button>
                );
            }
        }
        else {
            if (currentPage <= 3) {
                for (let i = 1; i <= 5; i++) {
                    items.push(
                        <button className="pagination-button" key={i} disabled={i === currentPage} onClick={() => handlePageChange(i)}> {i} </button>
                    );
                }
                items.push(
                    popover("right-ellipsis")
                )
            }
            else if (totalPage - currentPage <= 2) {
                items.push(
                    popover("left-ellipsis")
                )
                for (let i = totalPage - 4; i <= totalPage; i++) {
                    items.push(
                        <button className="pagination-button" key={i} disabled={i === currentPage} onClick={() => handlePageChange(i)}> {i} </button>
                    );
                }
            }
            else {
                items.push(
                    popover("left-ellipsis")
                )
                for (let i = currentPage - 2; i <= currentPage + 2; i++) {
                    items.push(
                        <button className="pagination-button" key={i} disabled={i === currentPage} onClick={() => handlePageChange(i)}> {i} </button>
                    );
                }
                items.push(
                    popover("right-ellipsis")
                )
            }
        }
        return items;
    };

    return (
        <div className="flex align-middle items-center justify-end gy-4 py-4">
            <div className="w-fit">
                {fixPageSize ? "" :
                    <div className="me-5 max-w-full min-w-12 w-fit text-left" >
                        <form className="">
                            <select value={perPage} style={{ width: "100%" }} onChange={(e) => { handlePerPageChange(e.target.value) }}>
                                <option value="1" >1 / page</option>
                                <option value="5" >5 / page</option>
                                <option value="10" >10 / page</option>
                                <option value="15" >15 / page</option>
                                <option value="30" >30 / page</option>
                                <option value="50" >50 / page</option>
                                <option value="100" >100 / page</option>
                            </select>
                        </form>
                    </div>
                }
            </div>
            <div className="">
                <button className="pagination-button rounded-s-lg" disabled={isFirstPage || totalPage === 0} onClick={() => handlePageChange(1)}>First</button>
                <button className="pagination-button" disabled={isFirstPage || totalPage === 0} onClick={() => handlePageChange(currentPage - 1)}>Previous</button>

                {renderPageItems()}

                <button className="pagination-button" disabled={isLastPage || totalPage === 0} onClick={() => handlePageChange(currentPage + 1)}>Next</button>
                <button className="pagination-button rounded-e-lg border-r-zinc-400" disabled={isLastPage || totalPage === 0} onClick={() => handlePageChange(totalPage)}>Last</button>
            </div>
        </div>
    );
}
