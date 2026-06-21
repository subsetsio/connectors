import json
from concurrent.futures import ThreadPoolExecutor
from subsets_utils import get

# max item
r = get("https://hacker-news.firebaseio.com/v0/maxitem.json", timeout=(10, 60))
print("maxitem:", r.json())

# a story, a comment, a poll, a deleted/null id, a job
for iid in (8863, 2921983, 126809, 1, 192327):
    r = get(f"https://hacker-news.firebaseio.com/v0/item/{iid}.json", timeout=(10, 60))
    print(iid, "->", json.dumps(r.json())[:240])

# concurrency sanity: fetch a small range
def f(i):
    return get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json", timeout=(10, 60)).json()

with ThreadPoolExecutor(max_workers=32) as ex:
    res = list(ex.map(f, range(8863, 8893)))
print("concurrent fetched:", len([x for x in res if x]), "of 30")
