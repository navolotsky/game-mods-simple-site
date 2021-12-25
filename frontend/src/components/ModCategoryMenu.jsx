import {useState} from 'react';
import DataSource from "../API/DataSource";
import OptionList from "./UI/OptionList"
import useSortedOptionListData from "../hooks/useSortedOptionListData";

const ModCategoryMenu = ({onOptionChange, gameId = null}) => {
    const defaultOptionConf = {id: null, name: "Any Category"};
    const [activeOptionId, setActiveOptionId] = useState(defaultOptionConf.id);

    function changeActiveOption(id) {
        setActiveOptionId(id);
        onOptionChange(id);
    }

    const [sortedCategories, isLoading, fetchingError] = useSortedOptionListData(
        DataSource.getModCategoriesForSidebar, [gameId], "name");

    const data = sortedCategories.map(({id, name, mods_number}) => {
        return {id, name, number: mods_number};
    })

    if (isLoading) return null;
    if (fetchingError) return <h2>Error occured: {fetchingError}</h2>;
    return (
        <OptionList data={data} onOptionChange={changeActiveOption}
                    activeOptionId={activeOptionId} defaultOptionConf={defaultOptionConf}/>
    );
};

export default ModCategoryMenu;
