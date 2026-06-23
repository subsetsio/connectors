import os, sys, ssl, httpx, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils
import subsets_utils.http_client as hc
ctx = ssl.create_default_context(); ctx.set_ciphers("DEFAULT")
hc._client = httpx.Client(timeout=60, headers=hc._client_config["headers"], follow_redirects=True, verify=ctx)
B = "https://clinicaltrials.gov/api/v2/studies"

fields = ",".join(["NCTId","Phase","EnrollmentCount","EnrollmentType","DesignAllocation",
  "DesignInterventionModel","DesignPrimaryPurpose","DesignMasking","MinimumAge","MaximumAge",
  "LocationFacility","LocationCity","LocationState","LocationCountry","LocationStatus"])
# interventional recruiting trial likely has phases, enrollment, design, locations
r = subsets_utils.get(B, params={"pageSize":2,"fields":fields,"filter.overallStatus":"RECRUITING",
  "query.term":"AREA[StudyType]INTERVENTIONAL"}, timeout=(10,90))
print("STATUS", r.status_code)
for s in r.json().get("studies", []):
    ps = s["protocolSection"]
    print("---")
    print("design:", json.dumps(ps.get("designModule",{}))[:400])
    locs = ps.get("contactsLocationsModule",{}).get("locations",[])
    print("nloc:", len(locs), "loc0:", json.dumps(locs[0]) if locs else None)
    print("elig:", json.dumps(ps.get("eligibilityModule",{}))[:200])
