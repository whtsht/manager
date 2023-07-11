import { Box, Button } from "@mui/material";
import CalendarMonthTwoToneIcon from "@mui/icons-material/CalendarMonthTwoTone";
import MenuBookTwoToneIcon from "@mui/icons-material/MenuBookTwoTone";
import liff from "@line/liff";

export function WebButton() {
    return (
        <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            sx={{ mr: 1 }}
            zIndex={100}
        >
            <CalendarMonthTwoToneIcon
                fontSize="large"
                style={{
                    transform: "scale(2.7)",
                    padding: "30px",
                    strokeWidth: "0.1",
                }}
            />
            <Button
                variant="contained"
                sx={{ mt: 2 }}
                onClick={() => liff.login()}
            >
                アプリに移動
            </Button>
        </Box>
    );
}

export function LineButton() {
    return (
        <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            sx={{ ml: 1 }}
            zIndex={100}
        >
            <img
                style={{ width: "100px" }}
                src="https://qr-official.line.me/gs/M_360aobyk_GW.png"
            ></img>
            <Button
                href="https://lin.ee/bi3aIvL"
                variant="contained"
                sx={{ mt: 2 }}
            >
                Line友達追加
            </Button>
        </Box>
    );
}

export function HowToUseButton() {
    return (
        <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            sx={{ m: 2 }}
            zIndex={50}
        >
            <MenuBookTwoToneIcon
                fontSize="large"
                style={{
                    transform: "scale(2.7)",
                    padding: "30px",
                    strokeWidth: "0.1",
                }}
            />
            <Button href="/how_to_use" variant="contained" sx={{ mt: 2 }}>
                使い方
            </Button>
        </Box>
    );
}
