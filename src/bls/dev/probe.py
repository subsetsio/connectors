import sys
import subsets_utils as su

UA = "subsets.io data connector (contact: nathansnellaert@gmail.com)"
su.configure_http(headers={"User-Agent": UA})

# 1) directory listing for a small survey 'ap'
for path in ["pub/time.series/ap/"]:
    r = su.get(f"https://download.bls.gov/{path}", timeout=(10,60))
    print("STATUS", path, r.status_code, len(r.text))
    print(r.text[:1500])
    print("=====")
