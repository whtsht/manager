/**
 * Designer    : 石川隼
 * Date        : 2023/6/13
 * Purpose     :
 */
import { Plan } from "../plan";
/**
 * Appサーバーに対して，HTTPリクエストを送信する．
 *
 * @param lineID   - ユーザーのLineID
 * @param plan     - 予定の情報
 * @returns
 */
async function modifyPlan(lineID: string, plan: Plan): Promise<boolean> {
  try {
    await fetch("/web/modifyPlan/", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        lineID: lineID,
        plan: plan,
      }),
    });
    return true;
  } catch (e) {
    return false;
  }
}

export { modifyPlan };
