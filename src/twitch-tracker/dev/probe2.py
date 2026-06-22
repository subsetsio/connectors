from subsets_utils import get
BASE = "https://twitchtracker.com/api"

logins = ["kaicenat","KaiCenat","xqc","kai_cenat","caseoh_","jynxzi","ironmouse",
          "hasanabi","pokimane","auronplay","ibai","tarik","summit1g","timthetatman",
          "loud_coringa","gaules","elspreen","rubius","fextralife","zackrawrr","tfue"]
for l in logins:
    r = get(f"{BASE}/channels/summary/{l}", timeout=(10.0,60.0))
    print(f"{l:20s} {r.status_code} {r.text[:120]}")
