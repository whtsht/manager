import { Box, Grid } from "@mui/material";
import MobilePhone from "./MobilePhone";

export default function Line() {
    return (
        <Box
            sx={{
                backgroundColor: "#ffffff",
                height: { md: "500px" },
            }}
        >
            <Grid
                container
                direction={"row"}
                paddingLeft={7}
                paddingRight={7}
                paddingTop={3}
                paddingBottom={3}
            >
                <Grid item xs={12} md={8}>
                    <h2>Lineアプリで手軽に管理</h2>
                    <p>
                        Lineを通じて簡単に予定を追加することができます．忘れてはいけないことがある，でも予定アプリを開くのは面倒というときにピッタリです．
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
                    <MobilePhone src="/screenshot-line.png" />
                </Grid>
            </Grid>
        </Box>
    );
}
