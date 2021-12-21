import {useState} from 'react';
import GameMenu from "../components/GameMenu";
import ModsFeed from "../components/ModsFeed";
import s from "./ModsFeedPage.module.css"
import ModCategoryMenu from "../components/ModCategoryMenu";

const ModsFeedPage = () => {
    const defaultOptionId = null
    const [chosenGameId, setChosenGameId] = useState(defaultOptionId)
    const [chosenCategoryId, setChosenCategoryId] = useState(defaultOptionId)
    return (
        <>
            <nav className={s.Sidebar}>
                <GameMenu onOptionChange={setChosenGameId} categoryId={chosenCategoryId}
                          defaultOptionId={defaultOptionId}/>
                <ModCategoryMenu onOptionChange={setChosenCategoryId} gameId={chosenGameId}
                                 defaultOptionId={defaultOptionId}/>
            </nav>
            <ModsFeed gameId={chosenGameId} categoryId={chosenCategoryId}/>
        </>
    );
};

export default ModsFeedPage;
