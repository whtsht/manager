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
import { useEffect } from "react";
import {
    Plan,
    PlanForm,
    dateTostring,
    planSchema,
    stringToDate,
} from "../Plan";
import { Button, DialogActions, Stack } from "@mui/material";
import { useFormik } from "formik";
import { ResponsiveDateTimePicker } from "./PlanAddDialog";
import { toast } from "react-toastify";

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
export default function PlanModifyDialog({
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
    const lineID = "a"; //liff.getContext()?.userId!;

    const innerHandleClose = () => {
        handleClose();
        window.setTimeout(formik.resetForm, 500);
    };

    const formik = useFormik<PlanForm>({
        initialValues: {
            title: "",
            notif: "",
            memo: "",
            allday: true,
            start: "",
            end: "",
        },
        validationSchema: planSchema,
        onSubmit: async (data) => {
            const newPlan: Plan = {
                id: plan!.id,
                lineID,
                title: data.title,
                detail: data.memo,
                notifTime: data.notif,
                allDay: data.allday ? data.start : null,
                start: !data.allday ? data.start : null,
                end: !data.allday ? data.end : null,
            } as Plan;
            await modifyPlan(newPlan);
            fetchPlanList();
            innerHandleClose();
            toast.success("予定を修正しました", {
                position: "bottom-right",
                autoClose: 3000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: false,
                draggable: true,
                progress: undefined,
                theme: "light",
            });
        },
    });

    useEffect(() => {
        if (plan) {
            formik.setFieldValue("title", plan.title);
            formik.setFieldValue("memo", plan.detail);
            formik.setFieldValue("notif", plan.notifTime);
            formik.setFieldValue("allday", !!plan.allDay);
            formik.setFieldValue("start", plan.allDay || plan.start);
            formik.setFieldValue("end", plan.end);
        }
    }, [plan]);

    return (
        <Dialog open={open} onClose={innerHandleClose} fullWidth>
            <Stack component="form" display="flex" gap={2} padding={3}>
                <TextField
                    id="予定名"
                    label="予定名"
                    variant="outlined"
                    value={formik.values.title}
                    onChange={(e) =>
                        formik.setFieldValue("title", e.target.value)
                    }
                    error={formik.touched.title && Boolean(formik.errors.title)}
                    helperText={formik.touched.title && formik.errors.title}
                />
                <TextField
                    value={formik.values.memo}
                    onChange={(e) =>
                        formik.setFieldValue("memo", e.target.value)
                    }
                    id="メモ"
                    label="メモ"
                    variant="outlined"
                    multiline
                    maxRows={3}
                    minRows={3}
                />
                <ResponsiveDateTimePicker
                    label="通知時間"
                    value={stringToDate(formik.values.notif)}
                    slotProps={{
                        textField: {
                            error:
                                formik.touched.notif &&
                                Boolean(formik.errors.notif),
                            helperText:
                                formik.touched.notif && formik.errors.notif,
                        },
                    }}
                    onChange={(e: Date | null) => {
                        if (e) {
                            formik.setFieldValue("notif", dateTostring(e));
                        }
                    }}
                />

                <FormControlLabel
                    control={
                        <Checkbox
                            checked={formik.values.allday}
                            onChange={(e) => {
                                formik.setFieldValue(
                                    "allday",
                                    e.target.checked
                                );
                            }}
                        />
                    }
                    label="終日"
                />

                <Box sx={{ width: "100%", height: "140px" }}>
                    {formik.values.allday ? (
                        <>
                            <ResponsiveDateTimePicker
                                label="開始時刻"
                                value={stringToDate(formik.values.start)}
                                slotProps={{
                                    textField: {
                                        error:
                                            formik.touched.start &&
                                            Boolean(formik.errors.start),
                                        helperText:
                                            formik.touched.start &&
                                            formik.errors.start,
                                    },
                                }}
                                onChange={(e: Date | null) => {
                                    if (e) {
                                        formik.setFieldValue(
                                            "start",
                                            dateTostring(e)
                                        );
                                    }
                                }}
                            />
                        </>
                    ) : (
                        <>
                            <ResponsiveDateTimePicker
                                label="開始時刻"
                                value={stringToDate(formik.values.start)}
                                slotProps={{
                                    textField: {
                                        error:
                                            formik.touched.start &&
                                            Boolean(formik.errors.start),
                                        helperText:
                                            formik.touched.start &&
                                            formik.errors.start,
                                    },
                                }}
                                onChange={(e: Date | null) => {
                                    if (e) {
                                        formik.setFieldValue(
                                            "start",
                                            dateTostring(e)
                                        );
                                    }
                                }}
                            />
                            <div style={{ height: "20px" }}></div>
                            <ResponsiveDateTimePicker
                                label="終了時刻"
                                value={
                                    formik.values.end
                                        ? stringToDate(formik.values.end)
                                        : null
                                }
                                slotProps={{
                                    textField: {
                                        error:
                                            formik.touched.end &&
                                            Boolean(formik.errors.end),
                                        helperText:
                                            formik.touched.end &&
                                            formik.errors.end,
                                    },
                                }}
                                onChange={(e: Date | null) => {
                                    if (e) {
                                        formik.setFieldValue(
                                            "end",
                                            dateTostring(e)
                                        );
                                    }
                                }}
                            />
                        </>
                    )}
                </Box>
                <DialogActions>
                    <Button
                        autoFocus
                        variant="outlined"
                        onClick={innerHandleClose}
                    >
                        閉じる
                    </Button>

                    <Button
                        autoFocus
                        variant="outlined"
                        onClick={() => formik.handleSubmit()}
                    >
                        保存
                    </Button>
                </DialogActions>
            </Stack>
        </Dialog>
    );
}
