/**
 * Designer    : 石川隼
 * Date        : 2023/6/13
 * Purpose     :
 */
import { Plan } from "../Plan";
/**
 * Appサーバーに対して，HTTPリクエストを送信する．
 *
 * @param plan     - 予定の情報
 * @returns
 */
async function modifyPlan(plan: Plan): Promise<boolean> {
    try {
        await fetch("/web/modifyPlan/", {
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

export { modifyPlan };
