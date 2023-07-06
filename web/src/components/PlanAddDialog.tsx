// /**
//  * Designer    : 菊地智遥
//  * Date        : 2023/7/4
//  * Purpose     : test
//  */

import React, { useEffect } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";
import { MobileDateTimePicker } from "@mui/x-date-pickers/MobileDateTimePicker";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";
import { addPlan } from "./AddPlan";
import { Plan } from "../Plan";
import liff from "@line/liff";
import { Stack } from "@mui/material";
import { dateTostring } from "../Plan";

function PlanAddDialog({
    open,
    handleClose,
    fetchPlanList,
}: {
    open: boolean;
    handleClose: () => void;
    fetchPlanList: () => void;
}) {
    const [ad, setAd] = React.useState(true);
    const [title, setTitle] = React.useState("");
    const [memo, setMemo] = React.useState("");
    const [notifTime, setNotifTime] = React.useState("");
    const [allDay, setAllDay] = React.useState<string | null>(null);
    const [start, setStart] = React.useState<string | null>(null);
    const [end, setEnd] = React.useState<string | null>(null);
    const lineID = "aaa"; //liff.getContext()?.userId!;

    useEffect(() => {
        if (ad) {
            setStart(null);
            setEnd(null);
        } else {
            setAllDay(null);
        }
    }, [ad]);

    const handleChange = (setFunc: (value: string) => void) => {
        return (e: Date | null) => {
            if (e !== null) {
                setFunc(dateTostring(e));
            }
        };
    };

    return (
        <Dialog open={open} onClose={handleClose} fullWidth>
            <Stack
                component="form"
                display="flex"
                justifyContent="center"
                gap={2}
                padding={3}
            >
                <TextField
                    onChange={(e) => setTitle(e.target.value)}
                    id="予定名"
                    label="予定名"
                    variant="outlined"
                />
                <TextField
                    onChange={(e) => setMemo(e.target.value)}
                    id="メモ"
                    label="メモ"
                    variant="outlined"
                    multiline
                    maxRows={3}
                    minRows={3}
                />
                <DateTimePicker
                    label="通知時間"
                    onChange={handleChange(setNotifTime)}
                />
                <FormControlLabel
                    control={
                        <Checkbox
                            defaultChecked
                            onChange={(e) => setAd(e.target.checked)}
                        />
                    }
                    label="終日"
                />

                <Box sx={{ width: "100%", height: "140px" }}>
                    {ad ? (
                        <>
                            <DateTimePicker
                                label="開始時刻"
                                sx={{ width: "100%" }}
                                onChange={handleChange(setAllDay)}
                            />
                        </>
                    ) : (
                        <>
                            <DateTimePicker
                                label="開始時刻"
                                sx={{ width: "100%" }}
                                onChange={handleChange(setStart)}
                            />
                            <div style={{ height: "20px" }}></div>
                            <DateTimePicker
                                label="終了時刻"
                                sx={{ width: "100%" }}
                                onChange={handleChange(setEnd)}
                            />
                        </>
                    )}
                </Box>
                <Button
                    variant="contained"
                    onClick={async () => {
                        const plan: Plan = {
                            lineID,
                            title: title,
                            detail: memo,
                            notifTime: notifTime,
                            allDay: allDay,
                            start: start,
                            end: end,
                        } as Plan;
                        await addPlan(lineID, plan);
                        handleClose();
                        fetchPlanList();
                    }}
                >
                    追加
                </Button>
            </Stack>
        </Dialog>
    );
}

export default PlanAddDialog;
