from subsets_utils import get
def j(u): return get(u, timeout=(10,60)).json()
B="https://api.nhtsa.gov/SafetyRatings"
years=j(B)["Results"]
print("years:", [y["ModelYear"] for y in years][:5], "... total", len(years))
# sample a few years to count VehicleIds
import itertools
total_vids=0; calls=0
for y in [2024, 2018, 2012, 2005, 1995]:
    makes=j(f"{B}/modelyear/{y}")["Results"]; calls+=1
    vids_year=0
    for mk in makes[:3]:
        models=j(f"{B}/modelyear/{y}/make/{mk['Make']}")["Results"]; calls+=1
        for md in models:
            vs=j(f"{B}/modelyear/{y}/make/{mk['Make']}/model/{md['Model']}")["Results"]; calls+=1
            vids_year+=len(vs)
    print(f"year {y}: {len(makes)} makes; first3-makes VehicleIds={vids_year}")
# one full rating record
vid=j(f"{B}/modelyear/2024/make/{makes[0]['Make']}/model/{makes[0]['Make']}")
print("sample done, calls used:", calls)
