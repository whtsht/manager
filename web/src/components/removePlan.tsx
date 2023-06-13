import { Plan } from "../plan";

async function removePlan(lineID: string, planID: string): Promise<boolean> {
  try {
    await fetch("/web/removePlan/", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        lineID: lineID,
        planID: planID,
      }),
    });
    return true;
  } catch (e) {
    return false;
  }
}

export { removePlan };
