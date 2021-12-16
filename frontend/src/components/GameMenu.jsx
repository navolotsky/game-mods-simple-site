import React, {useState} from 'react';
import s from "./GameMenu.module.css"
import {useFetching} from "../hooks/useFetching";
import DataSource from "../API/DataSource";

const GameMenu = ({onOptionChange, defaultOptionId = null}) => {
    const [activeOptionId, setActiveOptionId] = useState(defaultOptionId)
    const [sortedGames, setSortedGames] = useState([])

    function changeActiveOption(e, id) {
        setActiveOptionId(id)
        onOptionChange(id)
    };
    const [fetchGames, isLoading, fetchingError] = useFetching(async () => {
        const response = await DataSource.getGamesForSidebar()
        const games = response.data.sort((a, b) => {
            if (a.name < b.name) return -1;
            else if (a.name > b.name) return 1;
            else return 0;
        })
        setSortedGames(games)
    })

    useState(() => fetchGames())

    const defaultClasses = [s.game]

    function getClassName(optionId) {
        return (activeOptionId === optionId ? [...defaultClasses, s.activeOption] : [...defaultClasses, s.notActiveOption]).join(" ")
    }

    return (
        <table className={s.games}>
            <tbody>
            <tr className={getClassName(defaultOptionId)} key={defaultOptionId}
                onClick={e => changeActiveOption(e, defaultOptionId)}>
                <td className={s.gameName}>Any Game</td>
            </tr>
            {sortedGames.map(({id, name, mods_number}) =>
                <tr className={getClassName(id)} key={id}
                    onClick={(e) => changeActiveOption(e, id)}>
                    <td className={s.gameName}>{name}</td>
                    {mods_number && <td className={s.gameModsNumber}>{mods_number}</td>}
                </tr>)}
            </tbody>
        </table>
    );
};

export default GameMenu;
