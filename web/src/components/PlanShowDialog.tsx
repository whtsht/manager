/**
 * Designer    : 東間日向
 * Date        : 2023/6/17
 * Purpose     : 予定表示処理
 */

import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import { Plan, stringToDate } from "../Plan";
import Button from "@mui/material/Button";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import {
    Box,
    Checkbox,
    FormControlLabel,
    Stack,
    TextField,
} from "@mui/material";

/**
 * 予定表示画面
 * @param open          表示フラグ
 * @param closeHandle   閉じる関数
 * @param openModify    予定修正画面表示関数
 * @param openDelete    予定削除画面表示画面
 * @param plan          予定情報
 *
 * @returns
 */
function PlanShowDialog({
    open,
    handleClose,
    handleOpenModify,
    handleOpenDelete,
    plan,
}: {
    open: boolean;
    handleClose: () => void;
    handleOpenModify: () => void;
    handleOpenDelete: () => void;
    plan: Plan | null;
}) {
    if (plan == null) {
        return <></>;
    }
    console.log(plan);

    const ad = plan.allDay !== null;
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
                    id="予定名"
                    label="予定名"
                    variant="outlined"
                    value={plan.title}
                    InputProps={{ readOnly: true }}
                />
                <TextField
                    id="メモ"
                    label="メモ"
                    variant="outlined"
                    multiline
                    maxRows={3}
                    minRows={3}
                    value={plan.detail}
                    InputProps={{ readOnly: true }}
                />
                <DateTimePicker
                    label="通知時間"
                    value={stringToDate(plan.notifTime)}
                    readOnly
                />
                <FormControlLabel
                    control={<Checkbox checked disabled />}
                    label="終日"
                />

                <Box sx={{ width: "100%", height: "140px" }}>
                    {ad ? (
                        <>
                            <DateTimePicker
                                label="開始時刻"
                                sx={{ width: "100%" }}
                                value={stringToDate(plan.allDay!)}
                                readOnly
                            />
                        </>
                    ) : (
                        <>
                            <DateTimePicker
                                label="開始時刻"
                                sx={{ width: "100%" }}
                                value={stringToDate(plan.start!)}
                                readOnly
                            />
                            <div style={{ height: "20px" }}></div>
                            <DateTimePicker
                                label="終了時刻"
                                sx={{ width: "100%" }}
                                value={stringToDate(plan.end!)}
                                readOnly
                            />
                        </>
                    )}
                </Box>
                <ActionContents
                    handleClose={handleClose}
                    openModify={handleOpenModify}
                    openDelete={handleOpenDelete}
                />
            </Stack>
        </Dialog>
    );
}

function ActionContents({
    handleClose,
    openModify,
    openDelete,
}: {
    handleClose: () => void;
    openModify: () => void;
    openDelete: () => void;
}) {
    return (
        <DialogActions>
            <Button autoFocus onClick={handleClose}>
                閉じる
            </Button>
            <Button onClick={openModify} autoFocus>
                編集
            </Button>
            <Button onClick={openDelete} autoFocus>
                削除
            </Button>
        </DialogActions>
    );
}

export default PlanShowDialog;
