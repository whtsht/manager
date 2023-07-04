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

function PlanRemoveDialog({
    open,
    handleClose,
    plan,
    removePlan,
}: {
    open: boolean;
    handleClose: () => void;
    plan: Plan;
    removePlan: (id: number) => Promise<void>;
}) {
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
                        await removePlan(plan.id);
                        handleClose();
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
