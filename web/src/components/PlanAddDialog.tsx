/**
 * Designer    : 菊地智遥
 * Date        : 2023/7/4
 * Purpose     : 予定を追加する
 */

import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";
import {
    MobileDateTimePicker,
    MobileDateTimePickerSlotsComponentsProps,
} from "@mui/x-date-pickers/MobileDateTimePicker";
import {
    DateTimePicker,
    DateTimePickerSlotsComponentsProps,
} from "@mui/x-date-pickers/DateTimePicker";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";
import { useFormik } from "formik";
import { addPlan } from "./AddPlan";
import { Plan, PlanForm, planSchema, stringToDate } from "../Plan";
import liff from "@line/liff";
import { DialogActions, Stack } from "@mui/material";
import { dateTostring } from "../Plan";
import { DateOrTimeView } from "@mui/x-date-pickers";
import { toast } from "react-toastify";

export function ResponsiveDateTimePicker({
    label,
    slotProps,
    value,
    onChange,
}: {
    label: string;
    slotProps:
        | DateTimePickerSlotsComponentsProps<Date>
        | MobileDateTimePickerSlotsComponentsProps<Date, DateOrTimeView>
        | undefined;
    value: Date | null;
    onChange: (date: Date | null) => void;
}) {
    return (
        <>
            <MobileDateTimePicker
                label={label}
                sx={{ display: { xs: "flex", md: "none" } }}
                slotProps={
                    slotProps as MobileDateTimePickerSlotsComponentsProps<
                        Date,
                        DateOrTimeView
                    >
                }
                value={value}
                onChange={onChange}
            />
            <DateTimePicker
                label={label}
                sx={{ display: { xs: "none", md: "flex" } }}
                slotProps={
                    slotProps as DateTimePickerSlotsComponentsProps<Date>
                }
                value={value}
                onChange={onChange}
            />
        </>
    );
}

function PlanAddDialog({
    open,
    handleClose,
    fetchPlanList,
}: {
    open: boolean;
    handleClose: () => void;
    fetchPlanList: () => void;
}) {
    //const lineID = liff.getContext()?.userId!;
    const lineID = "a";

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
            formik.resetForm();
            const plan: Plan = {
                lineID,
                title: data.title,
                detail: data.memo,
                notifTime: data.notif,
                allDay: data.allday ? data.start : null,
                start: !data.allday ? data.start : null,
                end: !data.allday ? data.end : null,
            } as Plan;
            await addPlan(lineID, plan);
            handleClose();
            fetchPlanList();
            toast.success("予定を追加しました", {
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

    return (
        <Dialog open={open} onClose={innerHandleClose} fullWidth>
            <Stack component="form" display="flex" gap={2} padding={3}>
                <TextField
                    id="予定名"
                    label="予定名"
                    variant="outlined"
                    onChange={(e) =>
                        formik.setFieldValue("title", e.target.value)
                    }
                    error={formik.touched.title && Boolean(formik.errors.title)}
                    helperText={formik.touched.title && formik.errors.title}
                />
                <TextField
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
                    slotProps={{
                        textField: {
                            error:
                                formik.touched.notif &&
                                Boolean(formik.errors.notif),
                            helperText:
                                formik.touched.notif && formik.errors.notif,
                        },
                    }}
                    value={null}
                    onChange={(e: Date | null) => {
                        if (e) {
                            formik.setFieldValue("notif", dateTostring(e));
                        }
                    }}
                />

                <FormControlLabel
                    control={
                        <Checkbox
                            defaultChecked
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
                                value={null}
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
                                value={null}
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
                                value={null}
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
                        onClick={() => formik.handleSubmit()}
                    >
                        追加
                    </Button>
                </DialogActions>
            </Stack>
        </Dialog>
    );
}

export default PlanAddDialog;
