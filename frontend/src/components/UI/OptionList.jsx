import s from "./OptionList.module.css"

const OptionList = ({
                        data,
                        onOptionChange,
                        activeOptionId = null,
                        defaultOptionConf = {id: null, text: "Any"}
                    }) => {

    const defaultClasses = [s.option]

    function getClassName(optionId) {
        return (activeOptionId === optionId ?
            [...defaultClasses, s.activeOption] : [...defaultClasses, s.notActiveOption]
        ).join(" ")
    }

    return (
        <table className={s.options}>
            <tbody>
            <tr className={getClassName(defaultOptionConf.id)} key={defaultOptionConf.id}
                onClick={() => onOptionChange(defaultOptionConf.id)}>
                <td className={s.optionName}>Any Game</td>
            </tr>
            {data.map(({id, name, number}) =>
                <tr className={getClassName(id)} key={id}
                    onClick={(e) => onOptionChange(id)}>
                    <td className={s.optionName}>{name}</td>
                    {number && <td className={s.optionNumber}>{number}</td>}
                </tr>)}
            </tbody>
        </table>
    );
};

export default OptionList;
