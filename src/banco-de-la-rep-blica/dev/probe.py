import xml.etree.ElementTree as ET
from subsets_utils import get, configure_http

configure_http(headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://suameca.banrep.gov.co/estadisticas-economicas/",
})
NS = {
 "g":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
 "m":"http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
}
BASE="https://totoro.banrep.gov.co/nsi-jax-ws/rest/data/"
for df in ["DF_TRM_DAILY_HIST","DF_MONAGG_MONTHLY_HIST","DF_IBR_DAILY_HIST","DF_DTF_HIST","DF_DTF_TRIM_ANTICIPADO_HIST","DF_COLCAP_MONTHLY_HIST"]:
    r = get(BASE+df, timeout=(10,120))
    root = ET.fromstring(r.content)
    series = root.findall(".//g:Series", NS)
    print("="*60)
    print(df, "http", r.status_code, "n_series", len(series))
    for s in series[:3]:
        key = {v.get("id"):v.get("value") for v in s.findall("g:SeriesKey/g:Value", NS)}
        attrs = {v.get("id"):v.get("value") for v in s.findall("g:Attributes/g:Value", NS)}
        obs = s.findall("g:Obs", NS)
        first = obs[0] if obs else None
        last = obs[-1] if obs else None
        def od(o):
            if o is None: return None
            dim=o.find("g:ObsDimension",NS).get("value")
            val=o.find("g:ObsValue",NS)
            oa={v.get("id"):v.get("value") for v in o.findall("g:Attributes/g:Value",NS)}
            return (dim, val.get("value") if val is not None else None, oa)
        print("  KEY", key)
        print("  ATTR", attrs, "n_obs", len(obs))
        print("  first", od(first), "last", od(last))
