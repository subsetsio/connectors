import time
from subsets_utils import get, configure_http, transient_retry
from lxml import html as lh

configure_http(headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"})

CATS = ["content_management","programming_language","client_side_language","javascript_library",
"css_framework","web_server","web_panel","operating_system","web_hosting","data_center","proxy",
"dns_server","email_server","ssl_certificate","content_delivery","traffic_analysis","advertising",
"tag_manager","social_widget","site_element","structured_data","markup_language","character_encoding",
"image_format","top_level_domain","server_location","content_language"]


@transient_retry(attempts=6, min_wait=2, max_wait=30)
def fetch(url):
    r = get(url, timeout=(30.0, 120.0)); r.raise_for_status(); return r.text


def pick_table(doc):
    for t in doc.xpath("//table"):
        rows = t.xpath("./tr") or t.xpath("./tbody/tr")
        if not rows:
            continue
        head = [c for c in rows[0].xpath("./td|./th")]
        datarows = [row for row in rows if row.xpath("./th") and row.xpath("./td")]
        if len(datarows) >= 2 and len(head) >= 5:
            return head, datarows
    return None, None


for cat in CATS:
    try:
        text = fetch(f"https://w3techs.com/technologies/history_overview/{cat}/all/y")
    except Exception as e:
        print(f"{cat}: FETCH FAIL {type(e).__name__}")
        continue
    head, datarows = pick_table(lh.fromstring(text))
    if head is None:
        print(f"{cat}: NO TABLE FOUND")
        continue
    ndates = len(head) - 1  # minus leading empty cell
    mismatches = [(r.xpath('./th')[0].text_content().strip(), len(r.xpath('./td'))) for r in datarows if len(r.xpath('./td')) != ndates]
    # sample empties
    empties = 0
    for r in datarows:
        for c in r.xpath('./td'):
            if not c.text_content().strip():
                empties += 1
    print(f"{cat}: dates={ndates} rows={len(datarows)} mismatch={mismatches[:3]} empty_cells={empties}")
    time.sleep(1.5)
