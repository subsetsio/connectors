from subsets_utils import get, get_client
import xml.etree.ElementTree as ET
SDMX={"Accept":"application/vnd.sdmx.data+csv;version=1.0.0"}
NS={"s":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure"}

# REL_YEAR is dimension position 9 of 11. Key selects only that dim.
def year_key(year):
    parts = [""]*11
    parts[8] = year   # position 9 -> index 8
    return ".".join(parts)

# discover REL_YEAR codes
r=get("https://api.statistiken.bundesbank.de/rest/metadata/codelist/BBK/CL_BBK_RTD_REL_YEAR", timeout=(15,120))
root=ET.fromstring(r.content)
years=[c.get("id") for c in root.iterfind(".//s:Code", NS)]
print("REL_YEAR codes:", years[:5], "...", years[-3:], "n=", len(years))

client=get_client()
for y in [years[0], years[len(years)//2], years[-1]]:
    key=year_key(y)
    url=f"https://api.statistiken.bundesbank.de/rest/data/BBKRT/{key}"
    with client.stream("GET", url, headers=SDMX, timeout=(15,300)) as resp:
        st=resp.status_code
        nbytes=0; nlines=0; first=None
        if st==200:
            for line in resp.iter_lines():
                if nlines==0: first=line[:60]
                nlines+=1
                nbytes+=len(line)
        print(f"year={y} key={key!r} status={st} lines={nlines} approxbytes={nbytes} first={first!r}")
