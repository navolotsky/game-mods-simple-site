import {Route, Routes} from "react-router-dom";
import ModsFeed from "../pages/ModsFeed";
import NotFound from "../pages/NotFound";
import React from 'react';

const AppRouter = () => {
    return (<Routes>
        <Route path="/" element={<ModsFeed/>}/>
        <Route path="mods" element={<ModsFeed/>}/>
        <Route path="*" element={<NotFound/>}/>
    </Routes>)
};

export default AppRouter;
