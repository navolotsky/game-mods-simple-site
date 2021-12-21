import {useEffect, useState} from 'react';
import s from "./GameMenu.module.css"
import {useFetching} from "../hooks/useFetching";
import DataSource from "../API/DataSource";

const ModCategoryMenu = ({onOptionChange, gameId = null, defaultOptionId = null}) => {
    const [activeOptionId, setActiveOptionId] = useState(defaultOptionId)
    const [sortedCategories, setSortedCategories] = useState([])

    function changeActiveOption(e, id) {
        setActiveOptionId(id)
        onOptionChange(id)
    }

    const [fetchModCategories, isLoading, fetchingError] = useFetching(async (gameId) => {
        const response = await DataSource.getModCategoriesForSidebar(gameId)
        const mod_categories = response.data.sort((a, b) => {
            if (a.name < b.name) return -1;
            else if (a.name > b.name) return 1;
            else return 0;
        })
        setSortedCategories(mod_categories)
    })

    useState(() => fetchModCategories(gameId))
    useEffect(() => {
        fetchModCategories(gameId)
    }, [gameId])

    const defaultClasses = [s.game]

    function getClassName(optionId) {
        return (activeOptionId === optionId ? [...defaultClasses, s.activeOption] : [...defaultClasses, s.notActiveOption]).join(" ")
    }

    if (isLoading) return null;
    return (
        <table>
            <tbody>
            <tr className={getClassName(defaultOptionId)} key={defaultOptionId}
                onClick={e => changeActiveOption(e, defaultOptionId)}>
                <td className={s.gameName}>Any Category</td>
            </tr>
            {sortedCategories.map(({id, name, mods_number}) =>
                <tr className={getClassName(id)} key={id}
                    onClick={(e) => changeActiveOption(e, id)}>
                    <td className={s.gameName}>{name}</td>
                    {mods_number && <td className={s.gameModsNumber}>{mods_number}</td>}
                </tr>)}
            </tbody>
        </table>
    );
};

export default ModCategoryMenu;
