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
                        ManagerはLineを使って手軽に予定の追加，確認を行うことができます．また，Webアプリを使うと予定の詳細な設定ができます．
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
                    <MobilePhone />
                </Grid>
            </Grid>
        </Box>
    );
}
