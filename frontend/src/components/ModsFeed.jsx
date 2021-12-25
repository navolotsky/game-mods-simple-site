import {useEffect, useRef, useState} from "react";
import DataSource from "../API/DataSource";
import {useFetching} from "../hooks/useFetching";
import {useObserver} from "../hooks/useObserver";
import ModsFeedItem from "./ModsFeedItem";
import s from "./ModsFeed.module.css"

export default function ModsFeed({gameId = null, categoryId = null, limit = 10}) {
    const [renderedMods, setRenderedMods] = useState([])
    const [isThereNextPage, setIsThereNextPage] = useState(false)
    const [offset, setOffset] = useState(0)
    const feedTriggerRef = useRef()

    const [fetchMods, isModsLoading, modError] = useFetching(async (filters, limit, offset, clear = false) => {
            const feedTrigger = <div key="mods-feed-trigger" className={s.modsFeedTrigger} ref={feedTriggerRef}/>
            const response = await DataSource.getMods(filters, limit, offset)

            setIsThereNextPage(response.data.next !== null)
            setOffset(offset + response.data.results.length)

            const newRenderedMods = response.data.results.map(mod => <ModsFeedItem key={mod.id} mod={mod}/>)
            if (clear) renderedMods.length = 0;
            setRenderedMods(
                [
                    // remove trigger if any
                    ...renderedMods.slice(0, renderedMods.length - 2),
                    renderedMods[renderedMods.length - 1],
                    // insert trigger
                    ...newRenderedMods.slice(0, newRenderedMods.length - 1),
                    feedTrigger,
                    newRenderedMods[newRenderedMods.length - 1]])
        }
    )


    useState(() => fetchMods({gameId, categoryId}, limit, offset)) // enforce initial fetching

    // load next portion of content
    useObserver(feedTriggerRef, isThereNextPage, isModsLoading, () => fetchMods({gameId, categoryId}, limit, offset))

    // fully reload content because filter changed
    useEffect(() => {
        fetchMods({gameId, categoryId}, limit, 0, true)
    }, [gameId, categoryId])

    let content = renderedMods
    if (content.length === 0 && isModsLoading) content = <h2 className={s.loading}>...loading</h2>;
    else if (modError) content = <h2 className={s.error}>Error occured: {modError}</h2>;
    else if (!content.length) content = <h2 className={s.noContent}>No mods found!</h2>;
    return (
        <div className={s.ModsFeed}>
            {content}
        </div>
    )
};
