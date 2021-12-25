import {useState} from 'react';
import GameMenu from "../components/GameMenu";
import ModsFeed from "../components/ModsFeed";
import s from "./ModsFeedPage.module.css"
import ModCategoryMenu from "../components/ModCategoryMenu";

const ModsFeedPage = () => {
    const [chosenGameId, setChosenGameId] = useState()
    const [chosenCategoryId, setChosenCategoryId] = useState()
    return (
        <>
            <nav className={s.Sidebar}>
                <GameMenu onOptionChange={setChosenGameId} categoryId={chosenCategoryId}/>
                <ModCategoryMenu onOptionChange={setChosenCategoryId} gameId={chosenGameId}/>
            </nav>
            <ModsFeed gameId={chosenGameId} categoryId={chosenCategoryId}/>
        </>
    );
};

export default ModsFeedPage;
