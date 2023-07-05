import HowToUse from "./HowToUse";
import LoggedOut from "./components/LoggedOut";
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LoggedOut />} />
                <Route path="/how_to_use" element={<HowToUse />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
