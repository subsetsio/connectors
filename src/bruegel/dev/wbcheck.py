import httpx, time
FILES={
 "energy-crisis":"https://www.bruegel.org/sites/default/files/2026-06/policy_list_20260616.xlsx",
 "divisia":"https://www.bruegel.org/sites/default/files/2026-06/Divisia_database_ver12Jun2026.zip",
 "eu-labour":"https://www.bruegel.org/sites/default/files/2025-02/Download data 21.02.25.zip",
 "eu-renewables":"https://www.bruegel.org/sites/default/files/2025-12/EU renewables value tracker - Data - 03122025 - Bruegel 2.xlsx",
 "gas-imports":"https://www.bruegel.org/sites/default/files/2026-06/Gas Tracker update week 22 2026.zip",
 "gini":"https://www.bruegel.org/system/files/2024-02/Global_income_inequality_database_ver_9Feb2024.zip",
 "global-trade":"https://www.bruegel.org/sites/default/files/2026-06/2026-06-16 Global trade tracker.xlsx",
 "reer":"https://www.bruegel.org/sites/default/files/2026-06/REER_database_ver14Jun2026.zip",
 "russian":"https://www.bruegel.org/sites/default/files/2026-06/Russian foreign trade tracker - 2026-06-12.xlsx",
 "sovereign":"https://www.bruegel.org/system/files/2022-06/202004_Bruegel_sovereign_bond_-holding_dataset2.xlsx",
 "us-fms":"https://www.bruegel.org/sites/default/files/2026-05/bruegel_fms_dataset_third_release (1).xlsx",
}
def avail(u):
    for _ in range(3):
        try:
            r=httpx.get("https://archive.org/wayback/available",params={"url":u},timeout=40)
            if r.status_code==200:
                snap=r.json().get("archived_snapshots",{}).get("closest")
                return snap
        except Exception as e:
            time.sleep(2)
    return "ERR"
for k,u in FILES.items():
    s=avail(u)
    if isinstance(s,dict):
        print(f"{k}\tARCHIVED\t{s.get('timestamp')}\t{s.get('status')}")
    else:
        print(f"{k}\tNONE\t{s}")
