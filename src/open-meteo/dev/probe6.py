from subsets_utils import get
for m in ["MRI_AGCM3_2_S","EC_Earth3P_HR","MPI_ESM1_2_XR","CMCC_CM2_VHR4","NICAM16_8S"]:
    r=get("https://climate-api.open-meteo.com/v1/climate",
        params={"latitude":51.51,"longitude":-0.13,"start_date":"2000-01-01","end_date":"2000-01-02","models":m,"daily":"temperature_2m_max"},timeout=(10,120))
    d=r.json()
    if "error" in d: print(m,"ERROR",d.get("reason")); continue
    v=[x for x in d.get("daily",{}).get("temperature_2m_max",[]) if x is not None]
    print(f"{m}: nonnull={len(v)} sample={v[:2]}")
