import React from 'react';
import {useNavigate} from 'react-router-dom';
import DefaultButton from "./UI/buttons/DefaultButton";
import s from "./ModsFeedItem.module.css"

export default function ModsFeedItem({mod}) {
    const navigate = useNavigate()
    const date = mod.content.last_updated_at > mod.content.added_at ?
        `updated at ${new Date(mod.content.last_updated_at).toLocaleString()}`
        :
        `added at ${new Date(mod.content.added_at).toLocaleString()}`

    return (
        <article className={s.ModsFeedItem}>
            <header className={s.header}>
                <div className={s.heading}>
                    <div className={s.gameName}>{mod.game.name}</div>
                    <h2 className={s.title}>{mod.content.title}</h2>
                    <div className={s.versionNumber}>{mod.content.version_number}</div>
                </div>
                <ul className={s.categories}>
                    {mod.categories.map(category => <li className={s.categoryName}
                                                        key={category.id}>{category.name}</li>)}
                </ul>
            </header>
            <div className={s.content}>
                {mod.content.main_image && <img className={s.mainImage} src={mod.content.main_image.url} alt=""/>}
                <div className={s.description}>
                    {mod.content.description}
                </div>
            </div>
            <footer className={s.footer}>
                <div className={s.authorUsername}
                     title={date}>{mod.author.username}
                </div>
                <DefaultButton style={{margin: "10px"}} onClick={() => navigate(`/mods/${mod.id}`)}>
                    See more
                </DefaultButton>
            </footer>
        </article>
    )
}

