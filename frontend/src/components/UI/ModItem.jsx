import s from "./ModsItem.module.css";

function getDateString(updatedDate, addedDate) {
    return updatedDate > addedDate ?
        `updated at ${new Date(updatedDate).toLocaleString()}`
        :
        `added at ${new Date(addedDate).toLocaleString()}`;
}

const ModItem = ({mod, footerButton = null, onVersionChange = null, preview = false}) => {
    const date = getDateString(mod.content.last_updated_at, mod.content.added_at)

    function getVersionRowClassName(versionId) {
        switch (versionId) {
            case mod.requested_version_id: {
                if (mod.requested_version_id !== mod.default_version_id)
                    return [s.versionsTableRow, s.versionsTableRow_RequestedVersion].join(" ");
            }
            case mod.default_version_id:
                return [s.versionsTableRow, s.versionsTableRow_DefaultVersion].join(" ");
            default:
                return s.versionsTableRow;
        }
    }

    let images = null;
    if (!preview) {
        if (mod.content.main_image) {
            const mainImageId = mod.content.main_image.id;
            images = mod.content.images.filter(({id}) => id !== mainImageId);
        } else images = mod.content.images;
    }

    return (
        <article className={s.ModsItem}>
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
                {!preview && {images} &&
                <div className={s.images}>
                    {images.map(({id, url}) =>
                        (mod.content.main_image && (id === mod.content.main_image.id)) ?
                            null :
                            <img className={s.image} key={id} src={url} alt={""}/>)}
                </div>
                }
                {!preview && <table className={s.downloadLinksTable}>
                    <caption className={s.downloadLinksTableCaption}><b>Download Links</b></caption>
                    <thead className={s.downloadLinksTableHeader}>
                    <tr>
                        <th>Url</th>
                        <th>Comment</th>
                        <th>Updated</th>
                    </tr>
                    </thead>
                    <tbody>{mod.content.download_links.map(({id, url, comment, last_updated_at}) =>
                        <tr key={id} className={s.downloadLinksTableRow}>
                            <td><a href={url} target="_blank" rel="noopener noreferrer">{url}</a></td>
                            <td>{comment}</td>
                            <td>{new Date(last_updated_at).toLocaleString()}</td>
                        </tr>
                    )}</tbody>
                </table>
                }
                {!preview && <table className={s.versionsTable}>
                    <caption className={s.versionsTableCaption}><b>Versions</b></caption>
                    <thead className={s.versionsTableHeader}>
                    <tr>
                        <th>Number</th>
                        <th>Comment</th>
                        <th>Date</th>
                    </tr>
                    </thead>
                    <tbody>{mod.versions.map(({id, version_number, comment, last_updated_at, added_at}) =>
                        <tr key={id} className={getVersionRowClassName(id)}>
                            <td>{id !== mod.requested_version_id ?
                                <a href={`?version=${id}`}
                                   onClick={e => onVersionChange(e, id)}>{version_number}</a>
                                :
                                version_number
                            }</td>
                            <td>{comment}</td>
                            <td>{getDateString(last_updated_at, added_at)}</td>
                        </tr>
                    )}</tbody>
                </table>
                }
            </div>
            <footer className={s.footer}>
                <div className={s.authorUsername}
                     title={date}>{mod.author.username}
                </div>
                {footerButton}
            </footer>
        </article>
    )
};

export default ModItem;
