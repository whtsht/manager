import { Box } from "@mui/material";
import { LineButton, WebButton } from "./Buttons";

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
            <WebButton />
            <LineButton />
        </Box>
    );
}
