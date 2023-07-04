/**
 * Designer    : 小田桐光佑
 * Date        : 2023/6/
 * Purpose     :ログインをする前の機能概要やログインページへの誘導のためのwebページ
 */
import { Box, Stack } from "@mui/material";
import Footer from "./Footer";
import Header from "./Header";

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
            <Box sx={{ width: "100%" }}>
                <Stack>
                    <div
                        id="Home"
                        style={{ backgroundColor: "#deffcf", height: "600px" }}
                    >
                        <div
                            style={{
                                background: "url(/smartphone-white.png)",
                                backgroundSize: "100px",
                                width: "100px",
                                height: "100px",
                            }}
                        ></div>
                    </div>
                    <div
                        id={`${pages[0]}`}
                        style={{ backgroundColor: "#a6ff7d", height: "600px" }}
                    ></div>
                    <div
                        id={`${pages[1]}`}
                        style={{ backgroundColor: "#3fff3f", height: "600px" }}
                    ></div>
                    <div
                        id={`${pages[2]}`}
                        style={{ backgroundColor: "#a6ff7d", height: "700px" }}
                    ></div>
                    <Footer />
                </Stack>
            </Box>
        </>
    );
}

export default LoggedOut;
