"""Probe the FBI CDE signedurl -> S3 download chain for a couple of small datasets."""
import io
import os
import zipfile
import json

from subsets_utils import get

KEY = os.environ.get("FBI_CRIME_DATA_API_KEY", "DEMO_KEY")
SIGN = "https://api.usa.gov/crime/fbi/cde/s3/signedurl"


def signed(aws_file):
    r = get(SIGN, params={"key": aws_file, "API_KEY": KEY}, timeout=(10, 60))
    print("signedurl status", r.status_code, "->", r.text[:200])
    r.raise_for_status()
    return r.json()[aws_file]


def peek_csv(name, data: bytes, n=3):
    text = data.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    print(f"--- {name}: {len(data)} bytes, {len(lines)} lines")
    for ln in lines[:n]:
        print("   ", ln[:300])


for aws_file, member in [
    ("additional-datasets/territories/territories_1995_2024.csv", None),
    ("additional-datasets/srs/estimated_crimes_1979_2024.csv", None),
    ("additional-datasets/cargo-theft/CT_2013_2024.zip", "CT_2013_2024.csv"),
]:
    try:
        url = signed(aws_file)
        print("S3 url host:", url.split("/")[2])
        resp = get(url, timeout=(10, 120))
        resp.raise_for_status()
        content = resp.content
        if aws_file.endswith(".zip"):
            zf = zipfile.ZipFile(io.BytesIO(content))
            print("zip members:", zf.namelist())
            content = zf.read(member)
        peek_csv(aws_file, content)
    except Exception as e:
        print("ERROR on", aws_file, type(e).__name__, str(e)[:300])
    print()
