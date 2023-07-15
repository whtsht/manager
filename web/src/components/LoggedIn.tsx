/**
 * Designer    : 東間日向
 * Date        : 2023/6/20
 * Purpose     : ログイン後の画面処理
 */

import { useEffect, useState } from "react";
import Calendar from "./Calendar";
import UserShowDialog from "./UserShowDialog";
import PlanShowDialog from "./PlanShowDialog";
import liff from "@line/liff";
import { Plan } from "../Plan";
import PlanAddDialog from "./PlanAddDialog";
import PlanRemoveDialog from "./PlanRemoveDialog";
import PlanModifyDialog from "./PlanModifyDialog";
import { ToastContainer } from "react-toastify";

/**
 * Appサーバーに対してGETリクエストを送信し，予定情報のリストを取得する．
 *
 * @param lineID - ユーザーのLineID
 * @returns 予定情報のリスト
 */
async function getPlanList(): Promise<[Plan] | null> {
    const lineID = liff.getContext()?.userId;
    if (lineID === undefined) return null;
    try {
        const response = await fetch("/web/get_plan_list/", {
            method: "POST",
            headers: {
                "content-type": "application/json;charset=UTF-8",
            },
            body: JSON.stringify({
                lineID: lineID,
            }),
        });

        // 有効な値が返ってきたか確認
        if (!response.ok || response.status !== 200) {
            return null;
        }

        return response.json();
    } catch (_) {
        return null;
    }
}

/**
 * ログイン処理
 * カレンダー画面，予定表示画面，予定修正画面，予定削除画面，利用者画面を管理
 * @returns
 */
function LoggedIn() {
    const [planList, setPlanList] = useState<Plan[]>([]);
    const [plan, setPlan] = useState<null | Plan>(null);
    const [openAdd, setOpenAdd] = useState(false);
    const [openShow, setOpenShow] = useState(false);
    const [openDelete, setOpenDelete] = useState(false);
    const [openModify, setOpenModify] = useState(false);
    const [openUser, setOpenUser] = useState(false);
    const [date, setDate] = useState<Date | null>(null);

    const handleSetDate = (date: Date) => setDate(date);

    const fetchPlanList = async () => {
        const plans = await getPlanList();
        if (plans) {
            setPlanList(plans);
        }
    };

    useEffect(() => {
        fetchPlanList();
    }, []);

    return (
        <>
            <PlanShowDialog
                open={openShow}
                handleClose={() => setOpenShow(false)}
                handleOpenModify={() => setOpenModify(true)}
                handleOpenDelete={() => setOpenDelete(true)}
                plan={plan}
            />
            <PlanAddDialog
                open={openAdd}
                handleClose={() => setOpenAdd(false)}
                fetchPlanList={fetchPlanList}
                date={date!}
            />
            <PlanModifyDialog
                open={openModify}
                fetchPlanList={fetchPlanList}
                handleClose={() => setOpenModify(false)}
                plan={plan}
            />
            <PlanRemoveDialog
                open={openDelete}
                handleClose={() => setOpenDelete(false)}
                handleCloseShow={() => setOpenShow(false)}
                fetchPlanList={fetchPlanList}
                plan={plan}
            />

            <Calendar
                planList={planList}
                setPlan={(plan) => setPlan(plan)}
                handleOpenShow={() => setOpenShow(true)}
                handleOpenAdd={() => setOpenAdd(true)}
                handleOpenUser={() => setOpenUser(true)}
                handleSetDate={handleSetDate}
            />
            <UserShowDialog
                open={openUser}
                handleClose={() => setOpenUser(false)}
            />
            <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover={false}
                theme="light"
            />
        </>
    );
}

export default LoggedIn;
