import {useState} from 'react';
import DataSource from "../API/DataSource";
import useSortedOptionListData from "../hooks/useSortedOptionListData";
import OptionList from "./UI/OptionList";
import s from "./ModsFeed.module.css";

const GameMenu = ({onOptionChange, categoryId = null}) => {
    const defaultOptionConf = {id: null, name: "Any Game"};
    const [activeOptionId, setActiveOptionId] = useState(defaultOptionConf.id);

    function changeActiveOption(id) {
        setActiveOptionId(id);
        onOptionChange(id);
    }

    const [sortedGames, isLoading, fetchingError] = useSortedOptionListData(
        DataSource.getGamesForSidebar, [categoryId], "name");

    const data = sortedGames.map(({id, name, mods_number}) => {
        return {id, name, number: mods_number};
    })

    if (isLoading) return null;
    if (fetchingError) return <h2>Error occured: {fetchingError}</h2>;
    return (
        <OptionList data={data} onOptionChange={changeActiveOption}
                    activeOptionId={activeOptionId} defaultOptionConf={defaultOptionConf}/>
    );
};

export default GameMenu;
