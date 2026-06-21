from subsets_utils import get
import concurrent.futures as cf

BASE = "https://data.berkeleyearth.org/auto/Regional/TAVG/Text/{}-TAVG-Trend.txt"

continents = ["africa","asia","europe","north-america","south-america","oceania","antarctica"]
countries = """afghanistan albania algeria angola argentina armenia australia austria azerbaijan
bangladesh belarus belgium belize benin bhutan bolivia bosnia-and-herzegovina botswana brazil bulgaria burkina-faso burma burundi
cambodia cameroon canada chad chile china colombia congo costa-rica croatia cuba cyprus czech-republic
denmark dominican-republic ecuador egypt el-salvador eritrea estonia ethiopia
finland france gabon georgia germany ghana greece greenland guatemala guinea guyana
haiti honduras hungary iceland india indonesia iran iraq ireland israel italy ivory-coast
jamaica japan jordan kazakhstan kenya kuwait kyrgyzstan laos latvia lebanon lesotho liberia libya lithuania luxembourg
macedonia madagascar malawi malaysia mali mauritania mexico moldova mongolia montenegro morocco mozambique
namibia nepal netherlands new-zealand nicaragua niger nigeria north-korea norway oman
pakistan panama papua-new-guinea paraguay peru philippines poland portugal qatar romania russia rwanda
saudi-arabia senegal serbia sierra-leone slovakia slovenia somalia south-africa south-korea spain sri-lanka sudan suriname swaziland sweden switzerland syria
taiwan tajikistan tanzania thailand togo tunisia turkey turkmenistan
uganda ukraine united-arab-emirates united-kingdom united-states uruguay uzbekistan
venezuela vietnam yemen zambia zimbabwe""".split()
states = """alabama alaska arizona arkansas california colorado connecticut delaware florida georgia
hawaii idaho illinois indiana iowa kansas kentucky louisiana maine maryland massachusetts michigan minnesota mississippi missouri montana
nebraska nevada new-hampshire new-jersey new-mexico new-york north-carolina north-dakota ohio oklahoma oregon pennsylvania rhode-island
south-carolina south-dakota tennessee texas utah vermont virginia washington west-virginia wisconsin wyoming""".split()

cands = [(s,"continent") for s in continents] + [(s,"country") for s in countries] + [(s,"us-state") for s in states]

def check(item):
    slug, lvl = item
    try:
        r = get(BASE.format(slug), timeout=(8,30), headers={"Range":"bytes=0-200"})
        return (slug, lvl, r.status_code)
    except Exception as e:
        return (slug, lvl, "ERR:"+type(e).__name__)

ok, miss = [], []
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    for slug,lvl,st in ex.map(check, cands):
        if st in (200,206): ok.append((slug,lvl))
        else: miss.append((slug,lvl,st))

print("OK:", len(ok), "MISS:", len(miss))
print("MISSES:", miss)
import json
print(json.dumps(ok))
