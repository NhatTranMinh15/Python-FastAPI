import { FormEvent, useState } from "react";

type Props = {
    placeholder: string | null
    defaultValue: string
    setParamsFunction: any;
    style: Object
    className: string
}


export const SearchComponent = ({ className, placeholder, setParamsFunction, style, defaultValue }: Props) => {
    // console.log("render search");
    
    const [search, setSearch] = useState(defaultValue);

    function SubmitSearch(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        setParamsFunction("search", search)
    }

    return (
        <form className="" onSubmit={(e: FormEvent<HTMLFormElement>) => { SubmitSearch(e) }} style={{ width: "fit-content", ...style, }}>
            <input
                defaultValue={defaultValue}
                placeholder={placeholder ?? ""}
                className={"input search-placeholder !rounded-e-none " + className}
                id="search-input"
                name="search"
                onChange={(e) => setSearch(e.target.value)}
            />
            <button className={"!rounded-s-none button "} type="submit" id="search-button" onClick={() => { setParamsFunction("search", search) }}>
                Search
            </button>
        </form>
    );
}