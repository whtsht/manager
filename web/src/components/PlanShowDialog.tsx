/**
 * Designer    : 東間日向
 * Date        : 2023/6/17
 * Purpose     : 予定表示処理
 */

import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { Plan } from "../plan";
import Button from "@mui/material/Button";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import Textarea from "@mui/joy/Textarea";
import dayjs from "dayjs";
import CircleIcon from "@mui/icons-material/Circle";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";

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

    const TimeContents = plan.allDay ? (
        <>
            <TimeContent title="通知時間" time={plan.notifTime} />
            <TimeContent title="終日" time={plan.allDay} />
        </>
    ) : (
        <>
            <TimeContent title="通知時間" time={plan.notifTime} />
            <TimeContent title="開始時刻" time={plan.start!} />
            <TimeContent title="終了時刻" time={plan.end!} />
        </>
    );

    return (
        <Dialog
            open={open}
            onClose={handleClose}
            aria-labelledby="responsive-dialog-title"
        >
            <TitleContent title={plan?.title} />
            <DetailContent detail={plan?.detail} />
            {TimeContents}
            <ActionContent
                handleClose={handleClose}
                openModify={handleOpenModify}
                openDelete={handleOpenDelete}
            />
        </Dialog>
    );
}

function TitleContent({ title }: { title: string | undefined }) {
    return (
        <DialogTitle>
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    flexWrap: "wrap",
                    gap: "10px",
                }}
            >
                <CircleIcon style={{ color: "blue" }} />
                {title}
            </div>
        </DialogTitle>
    );
}

function DetailContent({ detail }: { detail: string | undefined }) {
    return (
        <div
            style={{
                flexWrap: "wrap",
                gap: "40px",
                padding: "0px 20px",
            }}
        >
            <p>メモ</p>
            <Textarea minRows={3} size="lg" disabled value={detail} />
        </div>
    );
}

function ActionContent({
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

function TimeContent({ title, time }: { title: string; time: string }) {
    console.log(dayjs(time));
    return (
        <DialogContent>
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-around",
                    gap: "20px",
                }}
            >
                <div style={{ width: "100px" }}>
                    <p style={{ fontSize: "16px", textAlign: "center" }}>
                        {title}
                    </p>
                </div>
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DateTimePicker
                        defaultValue={dayjs(time)}
                        ampm={false}
                        readOnly
                        format="YYYY/MM/DD  HH:mm"
                    />
                </LocalizationProvider>
            </div>
        </DialogContent>
    );
}

export default PlanShowDialog;
