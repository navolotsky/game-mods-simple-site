import {useEffect, useState} from 'react';
import {useFetching} from "../hooks/useFetching";

const useSortedOptionListData = (fetch_cb, fetch_cb_params, sort_field) => {
    const [sortedData, setSortedData] = useState([])

    const [fetchData, isLoading, fetchingError] = useFetching(async () => {
        const response = await fetch_cb(...fetch_cb_params)
        const data = sort_field ?
            response.data.sort((a, b) => {
                if (a[sort_field] < b[sort_field]) return -1;
                else if (a[sort_field] > b[sort_field]) return 1;
                else return 0;
            })
            :
            response.data;
        setSortedData(data)
    })

    useEffect(() => {
        fetchData()
    }, [fetch_cb, ...fetch_cb_params, sort_field])

    return [sortedData, isLoading, fetchingError]
};

export default useSortedOptionListData;
