import {Route, Routes} from "react-router-dom";
import NotFound from "../pages/NotFound";
import ModsFeedPage from "../pages/ModsFeedPage";
import ModPage from "./ModPage";

const AppRouter = () => {
    return (<Routes>
        <Route path="/" element={<ModsFeedPage/>}/>
        <Route path="mods" element={<ModsFeedPage/>}/>
        <Route path="mods/:id" element={<ModPage/>}/>
        <Route path="*" element={<NotFound/>}/>
    </Routes>)
};

export default AppRouter;
