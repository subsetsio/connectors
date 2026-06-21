import io, urllib.request, py7zr

def fetch(path):
    url = "ftp://ftp.mtps.gov.br/pdet/microdados/" + path
    return urllib.request.urlopen(url, timeout=120).read()

def inspect(path, label):
    print(f"\n===== {label}  ({path}) =====")
    raw = fetch(path)
    print("compressed bytes:", len(raw))
    with py7zr.SevenZipFile(io.BytesIO(raw)) as z:
        names = z.getnames()
        print("members:", names)
        data = z.read()
    for nm, bio in data.items():
        b = bio.read()
        txt = b.decode("latin-1", "replace")
        lines = txt.splitlines()
        print(f"  member {nm!r}: {len(b)} bytes, {len(lines)} lines")
        for i, ln in enumerate(lines[:3]):
            print(f"    L{i}: {ln[:300]}")
        # delimiter guess
        if lines:
            print("    header cols (;):", len(lines[0].split(';')))

# small ones first
inspect("NOVO%20CAGED/2026/202604/CAGEDEXC202604.7z", "NOVO CAGED EXC (tiny)")
inspect("NOVO%20CAGED/2026/202604/CAGEDFOR202604.7z", "NOVO CAGED FOR")
