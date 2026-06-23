import os, sys, ssl, httpx, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils
import subsets_utils.http_client as hc
ctx = ssl.create_default_context(); ctx.set_ciphers("DEFAULT")
hc._client = httpx.Client(timeout=60, headers=hc._client_config["headers"], follow_redirects=True, verify=ctx)
B = "https://clinicaltrials.gov/api/v2/studies"

fields = ",".join([
    "NCTId","BriefTitle","OfficialTitle","OverallStatus","StudyType","Phase",
    "EnrollmentCount","EnrollmentType","StartDate","PrimaryCompletionDate","CompletionDate",
    "StudyFirstPostDate","LastUpdatePostDate","WhyStopped",
    "LeadSponsorName","LeadSponsorClass","CollaboratorName","CollaboratorClass",
    "ResponsiblePartyType","Condition","InterventionType","InterventionName",
    "PrimaryOutcomeMeasure","PrimaryOutcomeTimeFrame","SecondaryOutcomeMeasure","SecondaryOutcomeTimeFrame",
    "DesignAllocation","DesignInterventionModel","DesignPrimaryPurpose","DesignMasking",
    "Sex","MinimumAge","MaximumAge","HealthyVolunteers",
    "LocationFacility","LocationCity","LocationState","LocationZip","LocationCountry","LocationStatus",
])
# find a study with rich data: search for an interventional one with results
r = subsets_utils.get(B, params={"pageSize": 1, "fields": fields, "query.term":"cancer", "filter.overallStatus":"COMPLETED"}, timeout=(10,90))
print("STATUS", r.status_code)
if r.status_code!=200:
    print(r.text[:300]); sys.exit()
d = r.json()
print(json.dumps(d["studies"][0], indent=1)[:4000])
