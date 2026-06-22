import asyncio
from playwright.async_api import async_playwright
URL="https://hgk.tjj.beijing.gov.cn/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber=60Y-1-03-N&queryCondition.objectType=04&queryCondition.objectCode=0100&yhid=guest&netType=2"
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(headless=True)
        ctx=await b.new_context()
        page=await ctx.new_page()
        caps=[]
        def on_req(req):
            if "QueryReportAction!" in req.url:
                caps.append((req.method, req.url.split("!")[1].split("?")[0], req.post_data))
        page.on("request", on_req)
        await page.goto(URL, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(3000)
        await b.close()
        for m,name,pd in caps:
            print("###",name)
            print("  ",pd)
asyncio.run(main())
