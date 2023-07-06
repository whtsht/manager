/**
 * Designer    : 石川隼
 * Date        : 2023/6/15
 * Purpose     :
 */
import { Plan } from "../Plan";
/**
 * 予定修正画面
 *
 * @param open          - 表示フラグ
 * @param handleClose   - 閉じる関数
 * @param plan          - 予定情報
 * @returns dialog      - ダイアログ表示のコンポーネント
 */

import Dialog from "@mui/material/Dialog";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import React, { useState } from "react";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DemoContainer, DemoItem } from "@mui/x-date-pickers/internals/demo";
import { Button } from "@mui/material";
import { modifyPlan } from "./ModifyPlan";

function PlanModifyDialog({
    open,
    handleClose,
    plan,
}: {
    open: boolean;
    handleClose: () => void;
    plan: Plan;
}) {
    return <></>;
    // const [check, setCheck] = useState(false);
    // const [ad, setAd] = React.useState(true);
    // const [title, setTitle] = React.useState("");
    // const [memo, setMemo] = React.useState("");
    // const [notifTime, setNotifTime] = React.useState("");
    // const [allDay, setAllDay] = React.useState("");
    // const [start, setStart] = React.useState("");
    // const [end, setEnd] = React.useState("");
    //
    // return (
    //     <Dialog open={open} onClose={handleClose}>
    //         <Box
    //             component="form"
    //             sx={{
    //                 "& > :not(style)": { m: 1, width: "500px" },
    //             }}
    //             noValidate
    //             autoComplete="off"
    //         >
    //             <TextField
    //                 onChange={(e) => setTitle(e.target.value)}
    //                 id="予定名"
    //                 label="予定名"
    //                 value={plan.title}
    //                 variant="outlined"
    //             />
    //             <TextField
    //                 onChange={(e) => setTitle(e.target.value)}
    //                 id="メモ"
    //                 label="メモ"
    //                 value={plan.detail}
    //                 variant="outlined"
    //             />
    //
    //             <LocalizationProvider dateAdapter={AdapterDayjs}>
    //                 <DemoContainer components={["DateTimePicker"]}>
    //                     <DemoItem label={"通知時間"}>
    //                         <DateTimePicker
    //                             value={dayjs(
    //                                 plan.notifTime,
    //                                 "YYYY/MM/DDThh:mm"
    //                             )}
    //                             views={[
    //                                 "year",
    //                                 "month",
    //                                 "day",
    //                                 "hours",
    //                                 "minutes",
    //                             ]}
    //                             onChange={(e: Dayjs | null) =>
    //                                 setNotifTime(e!.format("YYYY/MM/DDThh:mm"))
    //                             }
    //                         />
    //                     </DemoItem>
    //                 </DemoContainer>
    //             </LocalizationProvider>
    //             <FormControlLabel
    //                 control={
    //                     <Checkbox onChange={(e) => setAd(e.target.checked)} />
    //                 }
    //                 label="終日"
    //             />
    //
    //             {ad ? (
    //                 <LocalizationProvider dateAdapter={AdapterDayjs}>
    //                     <DemoContainer components={["DateTimePicker"]}>
    //                         <DemoItem label={"開始時間"}>
    //                             <DateTimePicker
    //                                 value={dayjs(
    //                                     plan.start,
    //                                     "YYYY/MM/DDThh:mm"
    //                                 )}
    //                                 views={[
    //                                     "year",
    //                                     "month",
    //                                     "day",
    //                                     "hours",
    //                                     "minutes",
    //                                 ]}
    //                                 onChange={(e: Dayjs | null) =>
    //                                     setAllDay(e!.format("YYYY/MM/DDThh:mm"))
    //                                 }
    //                             />
    //                         </DemoItem>
    //                     </DemoContainer>
    //                 </LocalizationProvider>
    //             ) : (
    //                 <LocalizationProvider dateAdapter={AdapterDayjs}>
    //                     <DemoContainer components={["DateTimePicker"]}>
    //                         <DemoItem label={"開始時間"}>
    //                             <DateTimePicker
    //                                 value={dayjs(
    //                                     plan.start,
    //                                     "YYYY/MM/DDThh:mm"
    //                                 )}
    //                                 views={[
    //                                     "year",
    //                                     "month",
    //                                     "day",
    //                                     "hours",
    //                                     "minutes",
    //                                 ]}
    //                                 onChange={(e: Dayjs | null) =>
    //                                     setStart(e!.format("YYYY/MM/DDThh:mm"))
    //                                 }
    //                             />
    //                         </DemoItem>
    //                         <DemoItem label={"終了時間"}>
    //                             <DateTimePicker
    //                                 value={dayjs(plan.end, "YYYY/MM/DDThh:mm")}
    //                                 views={[
    //                                     "year",
    //                                     "month",
    //                                     "day",
    //                                     "hours",
    //                                     "minutes",
    //                                 ]}
    //                                 onChange={(e: Dayjs | null) =>
    //                                     setEnd(e!.format("YYYY/MM/DDThh:mm"))
    //                                 }
    //                             />
    //                         </DemoItem>
    //                     </DemoContainer>
    //                 </LocalizationProvider>
    //             )}
    //             <Button
    //                 variant="contained"
    //                 onClick={() => {
    //                     const plan: Plan = {
    //                         title: title,
    //                         detail: memo,
    //                         notifTime: notifTime,
    //                         allDay: allDay,
    //                         start: start,
    //                         end: end,
    //                     } as Plan;
    //                     modifyPlan(plan);
    //                 }}
    //             >
    //                 修正する
    //             </Button>
    //         </Box>
    //     </Dialog>
    // );
}

export default PlanModifyDialog;
