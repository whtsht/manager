/**
 * Designer    : 石川隼
 * Date        : 2023/6/15
 * Purpose     :
 */
import { Plan } from "../Plan";
/**
 *
 *
 * @param open          - 表示フラグ
 * @param handleClose   - 閉じ関数
 * @param plan          - 予定の情報
 * @param removePlan    - 予定の削除
 * @returns dialog      - ダイアログ表示のコンポーネント
 */

import Dialog from "@mui/material/Dialog";
import Button from "@mui/material/Button";
import DialogActions from "@mui/material/DialogActions";
import DialogTitle from "@mui/material/DialogTitle";
import { toast } from "react-toastify";

async function removePlan(planID: string): Promise<boolean> {
    try {
        await fetch("/web/remove_plan/", {
            method: "POST",
            headers: {
                "content-type": "application/json;charset=UTF-8",
            },
            body: JSON.stringify({
                planID: planID,
            }),
        });
        return true;
    } catch (e) {
        return false;
    }
}

function PlanRemoveDialog({
    open,
    handleClose,
    handleCloseShow,
    fetchPlanList,
    plan,
}: {
    open: boolean;
    handleClose: () => void;
    handleCloseShow: () => void;
    fetchPlanList: () => void;
    plan: Plan | null;
}) {
    if (plan === null) {
        return <></>;
    }

    return (
        <Dialog
            open={open}
            onClose={handleClose}
            aria-labelledby="alert-dialog-title"
        >
            <DialogTitle id="alert-dialog-title">
                {"予定を削除しますか？"}
            </DialogTitle>
            <DialogActions>
                <Button
                    onClick={async () => {
                        await removePlan(plan.id.toString());
                        handleClose();
                        handleCloseShow();
                        fetchPlanList();
                        toast.success("予定を削除しました", {
                            position: "bottom-right",
                            autoClose: 3000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: false,
                            draggable: true,
                            progress: undefined,
                            theme: "light",
                        });
                    }}
                >
                    はい
                </Button>
                <Button onClick={handleClose} autoFocus>
                    いいえ
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default PlanRemoveDialog;
