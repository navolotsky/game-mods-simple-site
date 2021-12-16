import {useEffect, useRef} from "react";

export const useObserver = (ref, canLoad, isLoading, callback) => {
    const observerRef = useRef()
    useEffect(() => {
        if (isLoading) return;
        if (observerRef.current) observerRef.current.disconnect();

        const cb = function (entries) {
            if (entries[0].isIntersecting && canLoad) {
                callback()
            }
        };
        observerRef.current = new IntersectionObserver(cb)
        if (ref.current) observerRef.current.observe(ref.current);
    }, [isLoading])
}
