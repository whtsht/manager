import HowToUse from "./HowToUse";
import LoggedOut from "./components/LoggedOut";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import liff from "@line/liff";
import LoggedIn from "./components/LoggedIn";

function isLoggedIn(): boolean {
    try {
        return liff.isLoggedIn();
    } catch (e) {
        return false;
    }
}

function App() {
    console.log(isLoggedIn());
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={isLoggedIn() ? <LoggedIn /> : <LoggedOut />}
                />
                <Route path="/how_to_use" element={<HowToUse />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
