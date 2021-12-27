import {useNavigate} from 'react-router-dom';
import DefaultButton from "./UI/buttons/DefaultButton";
import ModItem from "./UI/ModItem";

export default function ModsFeedItem({mod}) {
    const navigate = useNavigate()
    return (
        <ModItem mod={mod}
                 footerButton={
                     <DefaultButton style={{margin: "10px"}} onClick={() => navigate(`/mods/${mod.id}`)}>
                         See more
                     </DefaultButton>}
                 preview={true}
        />
    )
}
