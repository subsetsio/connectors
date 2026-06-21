from subsets_utils import get
import json
for did in ["trade","TS058"]:
    d=get(f"https://api.beta.ons.gov.uk/v1/datasets/{did}",timeout=(10,60)).json()
    lv=d.get("links",{}).get("latest_version",{})
    print(f"\n=== {did} latest_version:", lv.get("href"))
    v=get(lv["href"],timeout=(10,60)).json()
    print("  downloads:", json.dumps(v.get("downloads",{})))
    print("  state:", v.get("state"), "| edition:", v.get("edition"), "| version:", v.get("version"))
    # check editions for an older version that has csv
    eds=get(f"https://api.beta.ons.gov.uk/v1/datasets/{did}/editions",timeout=(10,60)).json()
    for e in eds.get("items",[]):
        ed=e.get("edition")
        vs=get(f"https://api.beta.ons.gov.uk/v1/datasets/{did}/editions/{ed}/versions",timeout=(10,60)).json()
        print(f"  edition {ed}: {vs.get('total_count')} versions")
        for vv in vs.get("items",[]):
            print("    v",vv.get("version"),"downloads:",list(vv.get("downloads",{}).keys()))
