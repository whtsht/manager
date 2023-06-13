/**
 * Designer    : 東間日向
 * Date        : 2023/06/13
 * Purpose     : 予定情報の定義とFullCalendarとの連携
 */
import { EventClickArg, EventInput } from "@fullcalendar/core";

/**
 * 予定情報を表すインターフェース
 */
interface Plan {
    /**
     * 予定 ID
     */
    id: string;
    /**
     * 予定名
     */
    title: string;
    /**
     * 詳細
     */
    detail: string;
    /**
     * 通知時刻
     */
    notifTime: string;
    /**
     * 開始時刻(終日)
     */
    allDay: string | null;
    /**
     * 開始時刻
     */
    start: string | null;
    /**
     * 終了時刻
     */
    end: string | null;
}

/**
 * FullCalendarのeventClickの引数(EventClickArg)を予定情報(Plan)に変換する
 * @param info - FullCalendarのeventClickの引数
 * @returns
 */
function toPlan(info: EventClickArg): Plan {
    return {
        id: info.event.id,
        title: info.event.title,
        detail: info.event.extendedProps.detail,
        notifTime: info.event.extendedProps.notif_time,
        allDay: info.event.extendedProps.allDay,
        start: info.event.extendedProps.start,
        end: info.event.extendedProps.end,
    };
}

/**
 * 予定情報(Plan)をFullCalendarのEventInputに変換
 * @param plan - 予定情報
 * @returns
 */
function toEventInput(plan: Plan): EventInput {
    return {
        id: plan.id,
        title: plan.title,
    };
}

export type { Plan };
export { toPlan, toEventInput };
