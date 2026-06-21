import ftplib, io, re

ftp = ftplib.FTP("ftp.bom.gov.au", timeout=120)
ftp.login("anonymous", "x@y.com")
buf = io.BytesIO()
ftp.retrbinary("RETR /anon/gen/clim_data/IDCKWCDEA0/tables/stations_db.txt", buf.write)
ftp.quit()
text = buf.getvalue().decode("latin-1")
lines = [l for l in text.splitlines() if l.strip()]
print("lines:", len(lines))
pat = re.compile(r"^(\S+)\s+(\S+)\s+(\S+)\s+(.+?)\s+(\d{8}\.\.\d{0,8})\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*$")
ok=0; bad=[]
for l in lines:
    m = pat.match(l)
    if m: ok+=1
    else: bad.append(l)
print("matched:", ok, "unmatched:", len(bad))
for l in bad[:8]: print("  BAD:", repr(l))
for l in lines[:3]:
    m = pat.match(l)
    print("  parsed:", m.groups())
