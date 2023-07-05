import { Box } from "@mui/material";

export default function Footer() {
    return (
        <Box
            sx={{
                width: "100%",
                height: "auto",
                backgroundColor: "#555555",
                display: "flex",
                direction: "column",
                alignItems: "center",
                justifyContent: "center",
            }}
        >
            <p>
                2023&ensp;|&ensp;
                <a
                    style={{ color: "#000000" }}
                    href="https://github.com/whtsht/manager"
                >
                    Github
                </a>
            </p>
            &ensp;| &ensp;<a></a>
        </Box>
    );
}
