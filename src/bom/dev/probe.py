import ftplib, io, tarfile, csv

def fetch(path):
    ftp = ftplib.FTP("ftp.bom.gov.au", timeout=120)
    ftp.login("anonymous", "nathansnellaert@gmail.com")
    buf = io.BytesIO()
    ftp.retrbinary(f"RETR {path}", buf.write)
    ftp.quit()
    return buf.getvalue()

print("downloading tgz...")
data = fetch("/anon/gen/clim_data/IDCKWCDEA0.tgz")
print("tgz bytes:", len(data))
tf = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
members = tf.getmembers()
csvs = [m for m in members if m.name.endswith(".csv")]
print("total members:", len(members), "csv members:", len(csvs))
print("sample member names:")
for m in csvs[:5]:
    print("  ", m.name)
# inspect one csv
m = csvs[0]
print("=== first csv:", m.name)
raw = tf.extractfile(m).read().decode("latin-1")
for i, line in enumerate(raw.splitlines()[:16]):
    print(f"[{i}] {line!r}")
