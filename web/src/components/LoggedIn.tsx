/**
 * Designer    : 東間日向
 * Date        : 2023/6/20
 * Purpose     : ログイン後の画面処理
 */

import { useEffect, useState } from "react";
import Calendar from "./Calendar";
import UserShowDialog from "./UserShowDialog";
import PlanShowDialog from "./PlanShowDialog";
import { Plan } from "../plan";

/**
 * Appサーバーに対してGETリクエストを送信し，予定情報のリストを取得する．
 *
 * @param lineID - ユーザーのLineID
 * @returns 予定情報のリスト
 */
async function getPlanList(lineID: string): Promise<[Plan] | null> {
    try {
        const response = await fetch("/web/get_plan_list/", {
            method: "GET",
            headers: {
                "content-type": "application/json;charset=UTF-8",
            },
            body: JSON.stringify({
                lineID: lineID,
            }),
        });

        // 有効な値が返ってきたか確認
        if (!response.ok || response.status != 200) {
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
 * @param lineID    Line ID
 * @returns
 */
function LoggedIn({ lineID }: { lineID: string }) {
    const [planList, setPlanList] = useState<Plan[]>([]);
    const [plan, setPlan] = useState<null | Plan>(null);
    const [openAdd, setOpenAdd] = useState(false);
    const [openShow, setOpenShow] = useState(false);
    const [openDelete, setOpenDelete] = useState(false);
    const [openModify, setOpenModify] = useState(false);
    const [openUser, setOpenUser] = useState(false);

    useEffect(() => {
        (async () => {
            const plans = await getPlanList(lineID);
            if (plans) {
                setPlanList(plans);
            }
        })();
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
            <UserShowDialog />
            <Calendar
                planList={planList}
                setPlan={(plan) => setPlan(plan)}
                handleOpenShow={() => setOpenShow(true)}
                handleOpenAdd={() => setOpenAdd(true)}
                handleOpenUser={() => setOpenUser(true)}
            />
        </>
    );
}

export default LoggedIn;
