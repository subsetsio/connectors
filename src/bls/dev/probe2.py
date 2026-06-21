import subsets_utils as su
UA = "subsets.io data connector (contact: nathansnellaert@gmail.com)"
su.configure_http(headers={"User-Agent": UA})

# data file: stream first lines
r = su.get("https://download.bls.gov/pub/time.series/ap/ap.data.0.Current", timeout=(10,120))
lines = r.text.split("\n")
print("DATA header:", repr(lines[0]))
for l in lines[1:6]:
    print(repr(l))
print("ncols by tab:", [len(l.split('\t')) for l in lines[:4]])

# series file
r2 = su.get("https://download.bls.gov/pub/time.series/ap/ap.series", timeout=(10,120))
slines = r2.text.split("\n")
print("\nSERIES header:", repr(slines[0]))
for l in slines[1:3]:
    print(repr(l))

# period file
r3 = su.get("https://download.bls.gov/pub/time.series/ap/ap.period", timeout=(10,60))
print("\nPERIOD:")
print(r3.text)
