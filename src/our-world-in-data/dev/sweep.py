"""One-time reconnaissance: find every redistributable chart whose full CSV the
OWID Cloudflare worker cannot generate (persistent non-200). Confirms each
failure with sequential retries to avoid excluding charts that merely hit a
transient rate-limit during the sweep."""
import json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
import httpx

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
slugs = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/our-world-in-data/work/entity_union.json"))
print("sweeping", len(slugs), "charts")

client = httpx.Client(timeout=httpx.Timeout(connect=10, read=180, write=10, pool=10),
                      headers={"User-Agent": UA}, follow_redirects=True)

def check(slug):
    url = f"https://ourworldindata.org/grapher/{slug}.csv"
    try:
        # stream so we don't download the whole body; we only need the status
        with client.stream("GET", url, params={"csvType": "full", "useColumnShortNames": "true"}) as r:
            return slug, r.status_code
    except Exception as e:
        return slug, f"EXC:{type(e).__name__}"

failures = {}
done = 0
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(check, s): s for s in slugs}
    for f in as_completed(futs):
        slug, code = f.result()
        done += 1
        if code != 200:
            failures[slug] = code
        if done % 400 == 0:
            print(f"  {done}/{len(slugs)} done, {len(failures)} failures so far")

print("first-pass failures:", len(failures))

# Confirm each failure with up to 3 sequential retries (gentle).
confirmed = {}
for slug, code in sorted(failures.items()):
    ok = False
    last = code
    for i in range(3):
        time.sleep(2)
        _, c = check(slug)
        last = c
        if c == 200:
            ok = True
            break
    if not ok:
        confirmed[slug] = last
print("confirmed-unservable:", len(confirmed))
json.dump(sorted(confirmed.keys()),
          open("/Users/nathansnellaert/Documents/hardened/data/sources/our-world-in-data/work/unservable_slugs.json", "w"))
from collections import Counter
print("status breakdown:", Counter(confirmed.values()))
for s, c in sorted(confirmed.items()):
    print(" ", c, s)
