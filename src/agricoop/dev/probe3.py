import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
KEY=os.environ.get("DATA_GOV_IN_API_KEY","579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
r=get("https://api.data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de",
      params={"api-key":KEY,"format":"json","offset":0,"limit":5}, timeout=(10,120))
print("HTTP", r.status_code, "len", len(r.text))
print(r.text[:600])
