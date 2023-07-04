// /**
//  * Designer    : 菊地智遥
//  * Date        : 2023/7/4
//  * Purpose     : test
//  */

import React, { useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";
import { DemoContainer, DemoItem } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import { addPlan } from "./AddPlan";
import { Plan } from "../Plan";
import dayjs, { Dayjs } from "dayjs";

function PlanAddDialog({
    open,
    handleClose,
    lineID,
}: {
    open: boolean;
    handleClose: () => void;
    lineID: string;
}) {
    const [ad, setAd] = React.useState(true);
    const [title, setTitle] = React.useState("");
    const [memo, setMemo] = React.useState("");
    const [notifTime, setNotifTime] = React.useState("");
    const [allDay, setAllDay] = React.useState("");
    const [start, setStart] = React.useState("");
    const [end, setEnd] = React.useState("");

    return (
        <Dialog open={open} onClose={handleClose}>
            <Box
                component="form"
                sx={{
                    "& > :not(style)": { m: 1, width: "500px" },
                }}
                noValidate
                autoComplete="off"
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
                />
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DemoContainer components={["DateTimePicker"]}>
                        <DemoItem label={"通知時間"}>
                            <DateTimePicker
                                views={[
                                    "year",
                                    "month",
                                    "day",
                                    "hours",
                                    "minutes",
                                ]}
                                onChange={(e: Dayjs | null) =>
                                    setNotifTime(e!.format("YYYY/MM/DDThh:mm"))
                                }
                            />
                        </DemoItem>
                    </DemoContainer>
                </LocalizationProvider>
                <FormControlLabel
                    control={
                        <Checkbox
                            defaultChecked
                            onChange={(e) => setAd(e.target.checked)}
                        />
                    }
                    label="終日"
                />
                {ad ? (
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DemoContainer components={["DateTimePicker"]}>
                            <DemoItem label={"開始時間"}>
                                <DateTimePicker
                                    views={[
                                        "year",
                                        "month",
                                        "day",
                                        "hours",
                                        "minutes",
                                    ]}
                                    onChange={(e: Dayjs | null) =>
                                        setAllDay(e!.format("YYYY/MM/DDThh:mm"))
                                    }
                                />
                            </DemoItem>
                        </DemoContainer>
                    </LocalizationProvider>
                ) : (
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DemoContainer components={["DateTimePicker"]}>
                            <DemoItem label={"開始時間"}>
                                <DateTimePicker
                                    views={[
                                        "year",
                                        "month",
                                        "day",
                                        "hours",
                                        "minutes",
                                    ]}
                                    onChange={(e: Dayjs | null) =>
                                        setStart(e!.format("YYYY/MM/DDThh:mm"))
                                    }
                                />
                            </DemoItem>
                            <DemoItem label={"終了時間"}>
                                <DateTimePicker
                                    views={[
                                        "year",
                                        "month",
                                        "day",
                                        "hours",
                                        "minutes",
                                    ]}
                                    onChange={(e: Dayjs | null) =>
                                        setEnd(e!.format("YYYY/MM/DDThh:mm"))
                                    }
                                />
                            </DemoItem>
                        </DemoContainer>
                    </LocalizationProvider>
                )}
                <Button
                    variant="contained"
                    onClick={() => {
                        const plan: Plan = {
                            title: title,
                            detail: memo,
                            notifTime: notifTime,
                            allDay: allDay,
                            start: start,
                            end: end,
                        } as Plan;
                        addPlan(lineID, plan);
                    }}
                >
                    追加
                </Button>
            </Box>
        </Dialog>
    );
}

export default PlanAddDialog;
