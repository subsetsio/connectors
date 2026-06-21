import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json
from subsets_utils import get
for url in [
  "https://rss.marketingtools.apple.com/api/v2/us/apps/top-free/100/apps.json",
  "https://rss.marketingtools.apple.com/api/v2/us/music/most-played/100/songs.json",
  "https://rss.marketingtools.apple.com/api/v2/us/podcasts/top/100/podcasts.json",
]:
    r = get(url, timeout=(10,60))
    d = r.json()
    feed = d["feed"]
    print("URL", url, "status", r.status_code)
    print("  feed.updated:", feed.get("updated"))
    print("  n results:", len(feed.get("results", [])))
    e = feed["results"][0]
    print("  entry keys:", sorted(e.keys()))
    print("  sample id/name/kind:", e.get("id"), "|", e.get("name"), "|", e.get("kind"))
