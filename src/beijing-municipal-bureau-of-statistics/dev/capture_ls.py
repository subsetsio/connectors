import asyncio
from playwright.async_api import async_playwright
URL="https://hgk.tjj.beijing.gov.cn/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber=LS-1-07&queryCondition.objectType=04&queryCondition.objectCode=3700&yhid=guest&netType=2&queryCondition.dataSortTypeCode=01"
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(headless=True); ctx=await b.new_context(); page=await ctx.new_page()
        caps=[]; bodies={}
        page.on("request", lambda req: caps.append((req.url.split("!")[1].split("?")[0], req.post_data)) if "QueryReportAction!" in req.url else None)
        async def on_resp(resp):
            if "QueryReportAction!" in resp.url:
                try: bodies.setdefault(resp.url.split("!")[1].split("?")[0], await resp.text())
                except: pass
        page.on("response", on_resp)
        await page.goto(URL, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(3000); await b.close()
        for name,pd in caps: print("REQ",name,"::",pd)
        print("\n--- freqMask resp:", bodies.get("queryRptTimeFreqMask"))
        print("--- reportData resp head:", (bodies.get("queryReportData") or "")[:160])
asyncio.run(main())
