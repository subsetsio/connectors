import time
from subsets_utils import get, configure_http

configure_http(headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"})

FAIL = ["client_side_language", "site_element", "structured_data", "image_format"]

for slug in FAIL:
    for variant in [f"history_overview/{slug}/ms/y", f"history_overview/{slug}/all/y",
                    f"history_overview/{slug}", f"overview/{slug}"]:
        url = f"https://w3techs.com/technologies/{variant}"
        try:
            r = get(url, timeout=(30.0, 120.0))
            print(f"{slug:22} {variant:38} -> {r.status_code}  len={len(r.text)}")
        except Exception as e:
            print(f"{slug:22} {variant:38} -> EXC {type(e).__name__}")
        time.sleep(2)
    print()
