import { Box, Grid } from "@mui/material";
import MobilePhone from "./MobilePhone";

export default function Web() {
    return (
        <Box
            sx={{
                backgroundColor: "#a6ff7d",
                height: { md: "500px" },
            }}
        >
            <Grid
                container
                direction="row-reverse"
                paddingLeft={7}
                paddingRight={7}
                paddingTop={3}
                paddingBottom={3}
            >
                <Grid item xs={12} md={8}>
                    <h2>Webアプリでしっかり管理</h2>
                    <p>
                        Webアプリ版は開始時間，終了時間などを正確に管理したい場合に適しています．
                        またLineが入っていないPCなどでも素早く予定を確認することができます．
                    </p>
                </Grid>
                <Grid
                    item
                    xs={12}
                    md={4}
                    paddingTop={2}
                    display="flex"
                    justifyContent="center"
                >
                    <MobilePhone src="/screenshot-web.png" />
                </Grid>
            </Grid>
        </Box>
    );
}
