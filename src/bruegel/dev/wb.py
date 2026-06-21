import httpx, re
H={"User-Agent":"Mozilla/5.0"}
def latest_snapshot(url):
    # CDX API: newest snapshot
    r=httpx.get("https://web.archive.org/cdx/search/cdx",
        params={"url":url,"output":"json","limit":"-1","filter":"statuscode:200"}, headers=H, timeout=60)
    rows=r.json()
    if len(rows)<2: return None
    return rows[-1][1]  # timestamp
for page in ["https://www.bruegel.org/dataset/global-trade-tracker",
             "https://www.bruegel.org/publications/datasets/real-effective-exchange-rates-for-178-countries-a-new-database",
             "https://www.bruegel.org/dataset/us-foreign-military-sales"]:
    try:
        ts=latest_snapshot(page)
        print("PAGE", page.split('/')[-1][:36], "-> snapshot", ts)
        if not ts: continue
        arch=f"https://web.archive.org/web/{ts}id_/{page}"
        html=httpx.get(arch, headers=H, timeout=60, follow_redirects=True).text
        links=sorted(set(re.findall(r'/(?:sites/default|system)/files/[^"\')\s]+\.(?:xlsx|xls|csv|zip)', html)))
        print("   links:", links[:3], "| html len", len(html))
        if links:
            fu="https://www.bruegel.org"+links[0]
            fr=httpx.get(f"https://web.archive.org/web/{ts}id_/{fu}", headers=H, timeout=120, follow_redirects=True)
            print("   archived FILE:", fr.status_code, "bytes", len(fr.content), "|", links[0].split('/')[-1][:36])
    except Exception as e:
        print("PAGE", page.split('/')[-1][:36], "ERR", type(e).__name__, str(e)[:100])
