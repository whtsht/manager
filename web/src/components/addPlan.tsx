/**
 * Designer    : 菊地智遥
 * Date        : 2023/6/13
 * Purpose     : Appサーバーに対して，HTTPリクエストを送信する．
 */

import { Plan } from "../plan";

/**
 * Appサーバーに対して，HTTPリクエストを送信する．
 *
 * @param lineID   - ユーザーのLineID
 * @param plan     - 予定の情報
 * @returns
 */

async function addPlan(lineID: string, plan: Plan): Promise<boolean> {
  try {
    const response = await fetch("/web/add_plan/", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        lineID: lineID,
        plan: plan,
      }),
    });

    if (!response.ok || response.status != 200) {
      return false;
    }

    return true;
  } catch (e) {
    return false;
  }
}

export { addPlan };
