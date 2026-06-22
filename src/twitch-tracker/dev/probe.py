import json
from subsets_utils import get

BASE = "https://twitchtracker.com/api"

def show(url):
    r = get(url, timeout=(10.0, 60.0))
    print(f"\n=== {url}\nstatus={r.status_code} ct={r.headers.get('content-type')}")
    print("body:", r.text[:400])

# channels
for login in ["shroud", "ninja", "kaicenat"]:
    show(f"{BASE}/channels/summary/{login}")

# games by name and id
for g in ["Just Chatting", "League of Legends", "Grand Theft Auto V", "VALORANT", "509658"]:
    from urllib.parse import quote
    show(f"{BASE}/games/summary/{quote(g)}")

# error semantics: nonexistent channel
show(f"{BASE}/channels/summary/thischanneldoesnotexist999xyz")
