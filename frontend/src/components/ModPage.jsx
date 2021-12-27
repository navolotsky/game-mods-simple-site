import {useParams, useSearchParams} from "react-router-dom";
import {useFetching} from "../hooks/useFetching";
import DataSource from "../API/DataSource";
import {useEffect, useState} from "react";
import ModItem from "./UI/ModItem";

const ModPage = () => {
    const {id} = useParams();
    const [searchParams, setSearchParams] = useSearchParams();
    const {version: versionId} = Object.fromEntries(searchParams);
    const [data, setData] = useState(null);

    const [fetch, isLoading, error] = useFetching(async () => {
        const response = await DataSource.getMod(id, versionId);
        setData(response.data);
    })

    useEffect(() => {
        fetch();
    }, [id, versionId])

    function handleVersionChange(event, chosenVersionId) {
        event.preventDefault();
        setSearchParams({version: chosenVersionId});
    }

    return (
        <>
            {!isLoading && error && (
                error.response.status === 404 ? "mod or version not found" : "something went wrong")}
            {data && <ModItem mod={data} onVersionChange={handleVersionChange}/>}
        </>
    );
};

export default ModPage;
