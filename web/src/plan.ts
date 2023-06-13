import { EventClickArg, EventInput } from "@fullcalendar/core";

interface RawPlan {
    id: string;
    title: string;
    start: string | null;
    extendedProps: ExtendedProps;
}

interface ExtendedProps {
    lineID: string;
    detail: string;
    notifTime: string;
    allDay: string | null;
    end: string | null;
}

interface Plan {
    id: string;
    title: string;
    detail: string;
    notifTime: string;
    allDay: string | null;
    start: string | null;
    end: string | null;
}

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

function toEventInput(plan: Plan): EventInput {
    return {
        id: plan.id,
        title: plan.title,
    };
}

export type { RawPlan, Plan };
export { toPlan, toEventInput };
