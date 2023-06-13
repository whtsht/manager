/**
 * Designer    : 東間日向
 * Date        : 2023/6/13
 * Purpose     : Appサーバーから指定利用者の予定情報のリストを取得する
 */

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

export { getPlanList };
