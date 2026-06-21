import io, zipfile
from collections import Counter
from subsets_utils import get

def inspect(url, expected_fields, n_show=2, sample_lines=200000):
    print(f"\n===== {url} =====")
    r = get(url, timeout=(10,180))
    print("status", r.status_code, "bytes", len(r.content))
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    names = zf.namelist()
    print("members:", names)
    raw = zf.read(names[0])
    print("uncompressed bytes:", len(raw))
    text = raw.decode("latin-1")
    lines = text.split("\n")
    print("line count (split \\n):", len(lines))
    fc = Counter()
    bad = []
    for i, ln in enumerate(lines):
        if ln.strip()=="" : 
            continue
        nf = ln.count("\t")+1
        fc[nf]+=1
        if nf != expected_fields and len(bad)<3:
            bad.append((i, nf, ln[:160]))
    print("expected fields:", expected_fields)
    print("field-count distribution (top):", fc.most_common(6))
    print("sample mismatched lines:", bad)
    # show first record split
    first = [l for l in lines if l.strip()][0]
    cells = first.split("\t")
    print("first record cell count:", len(cells))
    print("first 6 cells:", cells[:6])

RCL = ['RECORD_ID','CAMPNO','MAKETXT','MODELTXT','YEARTXT','MFGCAMPNO','COMPNAME','MFGNAME','BGMAN','ENDMAN','RCLTYPECD','POTAFF','ODATE','INFLUENCED_BY','MFGTXT','RCDATE','DATEA','RPNO','FMVSS','DESC_DEFECT','CONEQUENCE_DEFECT','CORRECTIVE_ACTION','NOTES','RCL_CMPT_ID','MFR_COMP_NAME','MFR_COMP_DESC','MFR_COMP_PTNO','DO_NOT_DRIVE','PARK_OUTSIDE']
INV = ['NHTSA ACTION NUMBER','MAKE','MODEL','YEAR','COMPNAME','MFR_NAME','ODATE','CDATE','CAMPNO','SUBJECT','SUMMARY']

inspect("https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL_POST_2010.zip", len(RCL))
inspect("https://static.nhtsa.gov/odi/ffdd/inv/FLAT_INV.zip", len(INV))
