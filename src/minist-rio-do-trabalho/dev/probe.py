import io, os, tempfile, urllib.request, py7zr

def fetch(path):
    url = "ftp://ftp.mtps.gov.br/pdet/microdados/" + path
    return urllib.request.urlopen(url, timeout=180).read()

def inspect(path, label, maxlines=3):
    print(f"\n===== {label}  ({path}) =====")
    raw = fetch(path)
    print("compressed bytes:", len(raw))
    with tempfile.TemporaryDirectory() as td:
        with py7zr.SevenZipFile(io.BytesIO(raw)) as z:
            print("members:", z.getnames())
            z.extractall(path=td)
        for root,_,files in os.walk(td):
            for f in files:
                fp = os.path.join(root,f)
                sz = os.path.getsize(fp)
                with open(fp,'rb') as fh:
                    head = fh.read(2000)
                txt = head.decode("latin-1","replace")
                lines = txt.splitlines()
                print(f"  member {f!r}: {sz} bytes uncompressed")
                for i,ln in enumerate(lines[:maxlines]):
                    print(f"    L{i} ({len(ln.split(';'))} cols ;): {ln[:280]}")

inspect("NOVO%20CAGED/2026/202604/CAGEDEXC202604.7z", "NOVO CAGED EXC (tiny)")
inspect("NOVO%20CAGED/2026/202604/CAGEDFOR202604.7z", "NOVO CAGED FOR")
