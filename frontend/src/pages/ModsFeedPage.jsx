import React, {useState} from 'react';
import GameMenu from "../components/GameMenu";
import ModsFeed from "../components/ModsFeed";
import s from "./ModsFeedPage.module.css"

const ModsFeedPage = () => {
    const anyGameId = null
    const [chosenGameId, setChosenGameId] = useState(anyGameId)
    return (
        <>
            <nav className={s.Sidebar}>
                <GameMenu onOptionChange={setChosenGameId} defaultOptionId={anyGameId}/>
            </nav>
            <ModsFeed gameId={chosenGameId}/>
        </>
    );
};

export default ModsFeedPage;
