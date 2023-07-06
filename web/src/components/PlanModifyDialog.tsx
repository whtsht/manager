/**
 * Designer    : 石川隼
 * Date        : 2023/6/15
 * Purpose     :
 */

import Dialog from "@mui/material/Dialog";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import { useEffect, useState } from "react";
import { Plan, dateTostring, stringToDate } from "../Plan";
import { Button, DialogActions, Stack } from "@mui/material";

/**
 * Appサーバーに対して，HTTPリクエストを送信する．
 *
 * @param plan     - 予定の情報
 * @returns
 */
async function modifyPlan(plan: Plan): Promise<boolean> {
    try {
        await fetch("/web/modify_plan/", {
            method: "POST",
            headers: {
                "content-type": "application/json;charset=UTF-8",
            },
            body: JSON.stringify({
                plan: plan,
            }),
        });
        return true;
    } catch (e) {
        return false;
    }
}

/**
 * 予定修正画面
 *
 * @param open          - 表示フラグ
 * @param handleClose   - 閉じる関数
 * @param plan          - 予定情報
 * @returns dialog      - ダイアログ表示のコンポーネント
 */
function PlanModifyDialog({
    open,
    handleClose,
    fetchPlanList,
    plan,
}: {
    open: boolean;
    handleClose: () => void;
    fetchPlanList: () => void;
    plan: Plan | null;
}) {
    const [ad, setAd] = useState(true);
    const [title, setTitle] = useState("");
    const [memo, setMemo] = useState("");
    const [notifTime, setNotifTime] = useState("");
    const [allDay, setAllDay] = useState<string | null>(null);
    const [start, setStart] = useState<string | null>(null);
    const [end, setEnd] = useState<string | null>(null);
    const lineID = "aaa"; //liff.getContext()?.userId!;

    useEffect(() => {
        if (ad) {
            if (!allDay) setAllDay(start);
            setStart(null);
            setEnd(null);
        } else {
            if (!start) setStart(allDay);
            if (!end) setEnd(allDay);
            setAllDay(null);
        }
    }, [ad]);

    useEffect(() => {
        if (plan) {
            setAd(plan.allDay !== null);
            setTitle(plan.title);
            setMemo(plan.detail);
            setNotifTime(plan.notifTime);
            setAllDay(plan.allDay);
            setStart(plan.start);
            setEnd(plan.end);
        }
    }, [plan]);

    const handleChange = (setFunc: (value: string) => void) => {
        return (e: Date | null) => {
            if (e !== null) {
                setFunc(dateTostring(e));
            }
        };
    };

    if (plan === null) return <></>;

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
                    defaultValue={plan.title}
                />
                <TextField
                    onChange={(e) => setMemo(e.target.value)}
                    id="メモ"
                    label="メモ"
                    variant="outlined"
                    multiline
                    maxRows={3}
                    minRows={3}
                    defaultValue={plan.detail}
                />
                <DateTimePicker
                    label="通知時間"
                    onChange={handleChange(setNotifTime)}
                    defaultValue={stringToDate(plan.notifTime)}
                />
                <FormControlLabel
                    control={
                        <Checkbox
                            defaultChecked={plan.allDay !== null}
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
                                defaultValue={
                                    plan.allDay
                                        ? stringToDate(plan.allDay)
                                        : null
                                }
                            />
                        </>
                    ) : (
                        <>
                            <DateTimePicker
                                label="開始時刻"
                                sx={{ width: "100%" }}
                                onChange={handleChange(setStart)}
                                defaultValue={
                                    plan.start ? stringToDate(plan.start) : null
                                }
                            />
                            <div style={{ height: "20px" }}></div>
                            <DateTimePicker
                                label="終了時刻"
                                sx={{ width: "100%" }}
                                onChange={handleChange(setEnd)}
                                defaultValue={
                                    plan.end ? stringToDate(plan.end) : null
                                }
                            />
                        </>
                    )}
                </Box>
                <DialogActions>
                    <Button variant="outlined" onClick={handleClose}>
                        閉じる
                    </Button>
                    <Button
                        variant="outlined"
                        onClick={async () => {
                            const newPlan: Plan = {
                                id: plan.id,
                                lineID,
                                title: title,
                                detail: memo,
                                notifTime: notifTime,
                                allDay: allDay,
                                start: start,
                                end: end,
                            } as Plan;
                            await modifyPlan(newPlan);
                            handleClose();
                            fetchPlanList();
                        }}
                    >
                        保存
                    </Button>
                </DialogActions>
            </Stack>
        </Dialog>
    );
}

export default PlanModifyDialog;
