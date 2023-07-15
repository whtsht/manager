/**
 * Designer    : 東間日向
 * Date        : 2023/6/17
 * Purpose     : カレンダーの表示処理
 */

import FullCalendar from "@fullcalendar/react";
import allLocales from "@fullcalendar/core/locales-all";
import interactionPlugin from "@fullcalendar/interaction";
import dayGridPlugin from "@fullcalendar/daygrid";
import listPlugin from "@fullcalendar/list";
import { toPlan, Plan, toEventInput } from "../Plan";
import { useEffect } from "react";

/**
 * カレンダーを表示するコンポーネント
 * @param planList          - 予定情報のリスト
 * @param setPlan           - 利用者がクリックした予定を格納する関数
 * @param handleOpenShow    - 予定表示画面を表示する関数
 * @param handleOpenAdd     - 予定追加画面を表示する関数
 * @param handleOpenUser    - 利用者画面を表示する関数
 * @param handleSetDate     - 日付をセットする関数
 * @returns
 */
function Calendar({
    planList,
    setPlan,
    handleOpenShow,
    handleOpenAdd,
    handleOpenUser,
    handleSetDate,
}: {
    planList: Plan[];
    setPlan: (plan: Plan) => void;
    handleOpenShow: () => void;
    handleOpenAdd: () => void;
    handleOpenUser: () => void;
    handleSetDate: (date: Date) => void;
}) {
    useEffect(() => {
        const setIcon = (name: string, icon: string) => {
            const button = document.querySelector(
                `.fc-${name}-button`
            ) as HTMLElement;
            button.innerHTML = `<span class="material-symbols-outlined">${icon}</span>`;
        };
        setIcon("user", "person");
        setIcon("month", "calendar_month");
        setIcon("listMonth", "list");
    }, []);

    return (
        <FullCalendar
            plugins={[dayGridPlugin, interactionPlugin, listPlugin]}
            views={{
                month: {
                    type: "dayGridMonth",
                    displayEventTime: false,
                    titleFormat: {
                        year: "numeric",
                        month: "2-digit",
                    },
                },
            }}
            headerToolbar={{
                start: "prev,title,next",
                center: "",
                end: "month,listMonth,user",
            }}
            customButtons={{
                user: {
                    text: "",
                    click: handleOpenUser,
                },
            }}
            height="90vh"
            contentHeight="90vh"
            eventClick={(info) => {
                setPlan(toPlan(info));
                handleOpenShow();
            }}
            initialView={"month"}
            events={planList.map(toEventInput)}
            locales={allLocales}
            locale="ja"
            titleFormat={{
                month: "short",
                year: "numeric",
            }}
            dayCellContent={(e) => {
                return e.dayNumberText.replace("日", "");
            }}
            buttonText={{
                list: " ",
                month: " ",
            }}
            dateClick={(arg) => {
                handleSetDate(arg.date);
                handleOpenAdd();
            }}
        />
    );
}

export default Calendar;
