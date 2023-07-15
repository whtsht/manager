import HowToUse from "./HowToUse";
import LoggedOut from "./components/LoggedOut";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import liff from "@line/liff";
import LoggedIn from "./components/LoggedIn";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import ja from "date-fns/locale/ja";
import "react-toastify/dist/ReactToastify.css";

function isLoggedIn(): boolean {
    try {
        return liff.isLoggedIn();
    } catch (e) {
        return false;
    }
}

function App() {
    return (
        <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ja}>
            <BrowserRouter>
                <Routes>
                    <Route
                        path="/"
                        element={isLoggedIn() ? <LoggedIn /> : <LoggedOut />}
                    />
                    <Route path="/how_to_use" element={<HowToUse />} />
                </Routes>
            </BrowserRouter>
        </LocalizationProvider>
    );
}

export default App;
