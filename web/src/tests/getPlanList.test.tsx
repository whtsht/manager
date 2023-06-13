import { getPlanList } from "../components/getPlanList";

describe("test getPlanList", () => {
    const fetchOk = () => {
        global.fetch = jest.fn((_) => {
            const response: Response = {
                headers: new Headers(),
                ok: true,
                redirected: false,
                status: 200,
                statusText: "",
                type: "default",
                url: "",
                clone: function (): Response {
                    throw new Error("Function not implemented.");
                },
                body: null,
                bodyUsed: false,
                arrayBuffer: function (): Promise<ArrayBuffer> {
                    throw new Error("Function not implemented.");
                },
                blob: function (): Promise<Blob> {
                    throw new Error("Function not implemented.");
                },
                formData: function (): Promise<FormData> {
                    throw new Error("Function not implemented.");
                },
                json: async function (): Promise<any> {
                    return [];
                },
                text: function (): Promise<string> {
                    throw new Error("Function not implemented.");
                },
            };
            return Promise.resolve(response);
        });
    };

    const fetchErr = () => {
        global.fetch = jest.fn((_) => {
            const response: Response = {
                headers: new Headers(),
                ok: false,
                redirected: false,
                status: 500,
                statusText: "",
                type: "default",
                url: "",
                clone: function (): Response {
                    throw new Error("Function not implemented.");
                },
                body: null,
                bodyUsed: false,
                arrayBuffer: function (): Promise<ArrayBuffer> {
                    throw new Error("Function not implemented.");
                },
                blob: function (): Promise<Blob> {
                    throw new Error("Function not implemented.");
                },
                formData: function (): Promise<FormData> {
                    throw new Error("Function not implemented.");
                },
                json: async function (): Promise<any> {
                    throw new Error("Function not implemented.");
                },
                text: function (): Promise<string> {
                    throw new Error("Function not implemented.");
                },
            };
            return Promise.resolve(response);
        });
    };

    const mockLineID = "38291093";

    it("test getPlanList with good response", async () => {
        fetchOk();
        const planList = await getPlanList(mockLineID);
        expect(planList).toStrictEqual([]);
    });

    it("test getPlanList with bad response", async () => {
        fetchErr();
        const planList = await getPlanList(mockLineID);
        expect(planList).toStrictEqual(null);
    });
});
