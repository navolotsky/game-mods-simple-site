import './App.css';
import {BrowserRouter} from "react-router-dom";
import AppRouter from "./components/AppRouter";

function App() {

    return (
        <BrowserRouter>
            <main>
                <AppRouter/>
            </main>
        </BrowserRouter>)
}

export default App;
