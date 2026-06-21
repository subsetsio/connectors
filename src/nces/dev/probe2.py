from subsets_utils import get

def filename(table_file, y0, Y):
    span0=f"{(y0-1)%100:02d}{y0%100:02d}"; full0=str(y0); yy0=f"{y0%100:02d}"
    if span0 in table_file: form,tok0='span',span0
    elif full0 in table_file: form,tok0='full',full0
    elif yy0 in table_file: form,tok0='yy',yy0
    else: return None
    span=f"{(Y-1)%100:02d}{Y%100:02d}"; full=str(Y); yy=f"{Y%100:02d}"
    tokN={'span':span,'full':full,'yy':yy}[form]
    return table_file.replace(tok0,tokN)

tests=[("HD2024",2010),("F2324_F1A",2010),("SFA2324",2010),("GR200_24",2010),
       ("EF2024A",2012),("C2024_A",2010),("EFFY2024",2010),("DRVEF2024",2016),("SAL2024_IS",2005)]
for tf,Y in tests:
    fn=filename(tf,2024,Y)
    url=f"https://nces.ed.gov/ipeds/datacenter/data/{fn}.zip"
    r=get(url, timeout=(10,60))
    print(f"{tf} -> {Y}: {fn}.zip  HTTP {r.status_code}  {len(r.content) if r.status_code==200 else ''}")
