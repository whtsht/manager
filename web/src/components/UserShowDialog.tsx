// /**
//  * Designer    : 菊地智遥
//  * Date        : 2023/6/
//  * Purpose     : test
//  */

import liff from "@line/liff";
import { useState, useEffect } from "react";
import Dialog from "@mui/material/Dialog";
import { Button, Grid } from "@mui/material";

function getNameAndIcon(): [string | undefined, string | undefined] {
    const obj = liff.getDecodedIDToken();
    return [obj?.name, obj?.picture];
}

function UserShowDialog({
    open,
    handleClose,
}: {
    open: boolean;
    handleClose: () => void;
}) {
    const [name, setName] = useState<undefined | string>(undefined);
    const [icon, setIcon] = useState<undefined | string>(undefined);

    useEffect(() => {
        const [name_, icon_] = getNameAndIcon();
        setName(name_);
        setIcon(icon_);
    }, []);

    return (
        <Dialog onClose={handleClose} open={open}>
            <Grid
                container
                justifyContent="space-around"
                spacing={1}
                sx={{ padding: 2 }}
            >
                <Grid
                    item
                    xs={4}
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                >
                    <img
                        src={icon}
                        alt="アイコン"
                        style={{
                            borderRadius: "50%",
                            width: "45px",
                            height: "45px",
                        }}
                    />
                </Grid>
                <Grid item xs={8} textAlign="inherit">
                    <p>ログイン中のアカウント</p>
                    <h1
                        style={{
                            fontSize: "26px",
                            margin: "0 0 20px 0",
                        }}
                    >
                        {name}
                    </h1>
                </Grid>
                <Grid item xs={6} display="flex" justifyContent="center">
                    <Button variant="outlined" onClick={handleClose}>
                        閉じる
                    </Button>
                </Grid>
                <Grid
                    item
                    xs={6}
                    display="flex"
                    justifyContent="center"
                    marginBottom="5px"
                >
                    <Button
                        variant="outlined"
                        onClick={() => {
                            if (liff.isLoggedIn()) {
                                liff.logout();
                                window.location.reload();
                            }
                        }}
                    >
                        ログアウト
                    </Button>
                </Grid>
            </Grid>
        </Dialog>
    );
}

export default UserShowDialog;
