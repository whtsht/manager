/**
 * Designer    : 小田桐光佑，東間日向
 * Date        : 2023/7/5
 * Purpose     :ログインをする前の機能概要やログインページへの誘導のためのwebページ
 */
import { Box, Stack } from "@mui/material";
import Footer from "./Footer";
import Header from "./Header";
import Home from "./Home";
import Line from "./Line";
import Web from "./Web";
import GetStart from "./GetStart";

export const pages = ["Line", "Web", "始める"];

function LoggedOut() {
    // const handleButtonClick = () => {
    //     /**
    //      * ここに実際のlineログインの処理を追加する．
    //      **/
    //     window.open("https://example.com/line-login");
    // };

    return (
        <>
            <Header />
            <Box sx={{ p: 0, m: 0 }}>
                <Stack>
                    <Home />
                    <div
                        id={pages[0]}
                        style={{
                            position: "relative",
                            top: "-40px",
                        }}
                    ></div>
                    <Line />
                    <div
                        id={pages[1]}
                        style={{
                            position: "relative",
                            top: "-40px",
                        }}
                    ></div>
                    <Web />
                    <div
                        id={pages[2]}
                        style={{
                            position: "relative",
                            top: "-40px",
                        }}
                    ></div>
                    <GetStart />
                </Stack>
                <Footer />
            </Box>
        </>
    );
}

export default LoggedOut;
