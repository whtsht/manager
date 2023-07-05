import { Box, Button } from "@mui/material";
import CalendarMonthOutlinedIcon from "@mui/icons-material/CalendarMonthOutlined";
import TouchAppOutlinedIcon from "@mui/icons-material/TouchAppOutlined";

export default function GetStart() {
    return (
        <Box
            sx={{
                backgroundColor: "#fffff",
                height: { sm: "500px" },
            }}
            style={{ textAlign: "center" }}
        >
            <h2>初めてみましょう :)</h2>
            <Actions />

            <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                sx={{ m: 2 }}
                zIndex={50}
            >
                <TouchAppOutlinedIcon
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
        </Box>
    );
}

export function Actions() {
    const prop = {
        display: "flex",
        mt: { sx: 3, sm: 5 },
        gap: { sx: 5, sm: 10 },
        justifyContent: "center",
    };
    return (
        <Box sx={prop} alignItems="end" padding={2}>
            <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                sx={{ mr: 1 }}
                zIndex={100}
            >
                <CalendarMonthOutlinedIcon
                    fontSize="large"
                    style={{
                        transform: "scale(2.7)",
                        padding: "30px",
                        strokeWidth: "0.1",
                    }}
                />
                <Button variant="contained" sx={{ mt: 2 }}>
                    アプリに移動
                </Button>
            </Box>
            <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                sx={{ ml: 1 }}
                zIndex={100}
            >
                <img
                    style={{ width: "100px" }}
                    src="https://qr-official.line.me/gs/M_566fjjmf_GW.png"
                ></img>
                <Button variant="contained" sx={{ mt: 2 }}>
                    Line友達追加
                </Button>
            </Box>
        </Box>
    );
}
