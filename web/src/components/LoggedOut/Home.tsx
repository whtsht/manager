import { Box, Grid } from "@mui/material";
import MobilePhone from "./MobilePhone";
import { LineButton, WebButton } from "./Buttons";

export default function Home() {
    return (
        <Box
            sx={{
                backgroundColor: "#deffcf",
                height: { sm: "500px" },
            }}
        >
            <Grid container direction={"row-reverse"} sx={{ padding: 2 }}>
                <Grid item xs={12} sm={8}>
                    <p>予定管理をより手軽に！</p>
                    <h1>Guide me</h1>
                    <p>
                        Guide&nbsp;meはなインターフェースを提供する予定管理アプリです．
                        このアプリはLineアプリ，Webアプリ間で予定情報を共有することができます．
                        利用者の性格，ライフスタイルに合わせて多様な使い方ができます．
                    </p>
                    <Actions mobile={false} />
                </Grid>
                <Grid
                    item
                    xs={12}
                    sm={4}
                    paddingTop={2}
                    display="flex"
                    justifyContent="center"
                >
                    <MobilePhone />
                </Grid>
                <Grid item xs={12} sm={6} display={{ sx: "flex", sm: "none" }}>
                    <Actions mobile />
                </Grid>
            </Grid>
        </Box>
    );
}

export function Actions({ mobile }: { mobile: boolean }) {
    const prop = mobile
        ? {
              display: { xs: "flex", sm: "none" },
              mt: { sx: 3, sm: 5 },
              mr: { sx: 0, md: 15, lg: 40 },
              gap: { sx: 5, sm: 10 },
              justifyContent: { xs: "space-evenly" },
          }
        : {
              display: { xs: "none", sm: "flex" },
              mt: { sx: 3, sm: 5 },
              mr: { sx: 0, md: 15, lg: 40 },
              gap: { sx: 5, sm: 10 },
              justifyContent: { xs: "space-evenly" },
          };
    return (
        <Box sx={prop} alignItems="end" padding={2}>
            <WebButton />
            <LineButton />
        </Box>
    );
}
