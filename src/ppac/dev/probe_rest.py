import re, json
from subsets_utils import get

REST = {
 "consumption/products-wise":43, "production/petroleum-products":42,
 "prices/international-prices-of-crude-oil":30, "production/indigenous-crude-oil":3,
 "import-export":14, "natural-gas/production":170, "natural-gas/consumption":138,
 "production/crude-processing":41,
}
JS_CACHE={}
def page_html(p): return get(f"https://ppac.gov.in/{p}").text
def find_methods_in(html):
    return sorted({m for m in re.findall(r"AjaxController/(get[A-Za-z0-9_]+)\b", html)})

for p,pid in REST.items():
    h=page_html(p)
    methods=find_methods_in(h)
    # if no Data method inline, scan referenced local JS bundles
    if not any(not m.endswith("ChartData") for m in methods):
        for src in re.findall(r'<script[^>]+src="([^"]+\.js[^"]*)"', h):
            if "ppac.gov.in" in src and "/assets/" in src and src not in JS_CACHE:
                try: JS_CACHE[src]=get(src if src.startswith("http") else "https://ppac.gov.in"+src).text
                except Exception as e: JS_CACHE[src]=""
                mm=find_methods_in(JS_CACHE[src])
                if any(not m.endswith("ChartData") for m in mm):
                    methods=sorted(set(methods)|set(mm)); 
    fys=sorted(set(re.findall(r'<option value="(\d{4}-\d{4})"',h)))
    # reportBy options
    rb=re.findall(r'<option value="(\d)">([^<]*)</option>',h)
    data_methods=[m for m in methods if not m.endswith("ChartData")]
    print(f"{p:42s} pid={pid:<4} fys={fys} rb={rb[:4]} methods={data_methods}")
