from subsets_utils import get

# Global S3 text products
S3 = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/"
globals_ = [
    "Land_and_Ocean_complete.txt",
    "Complete_TAVG_complete.txt",
]
for f in globals_:
    u = S3 + f
    try:
        r = get(u, timeout=(10,120))
        lines = r.text.splitlines()
        print("====", f, r.status_code, len(r.text), "bytes,", len(lines), "lines")
        # find first data line and header columns
        data_start = None
        for i, ln in enumerate(lines):
            if ln.strip() and not ln.lstrip().startswith('%'):
                data_start = i; break
        # print column-header comment lines near data_start
        for ln in lines[max(0,data_start-6):data_start]:
            print("  HDR", repr(ln[:170]))
        for ln in lines[data_start:data_start+4]:
            print("  DAT", repr(ln[:170]))
        print("  LAST", repr(lines[-1][:170]))
    except Exception as e:
        print("ERR", f, type(e).__name__, e)
