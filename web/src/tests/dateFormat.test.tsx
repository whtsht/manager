import { dateTostring, stringToDate } from "../Plan";
import { parse } from "date-fns";

describe("test getPlanList", () => {
    it("test stringToDate", async () => {
        const expected = parse(
            "2021-08-21 09:00:00",
            "yyyy-MM-dd HH:mm:ss",
            new Date()
        );
        const received = stringToDate("2021-08-21T09:00");
        expect(received).toStrictEqual(expected);
    });

    it("test dateToString", async () => {
        const date = stringToDate("2021-08-21T09:00");
        const received = dateTostring(date);
        const expected = "2021/08/21T09:00";
        expect(received).toStrictEqual(expected);
    });
});
