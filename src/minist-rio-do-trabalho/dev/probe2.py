import io, os, tempfile, urllib.request, py7zr

def fetch_to_tmp(path, td):
    url = "ftp://ftp.mtps.gov.br/pdet/microdados/" + path
    p = os.path.join(td, "a.7z")
    with urllib.request.urlopen(url, timeout=180) as r, open(p,'wb') as o:
        import shutil; shutil.copyfileobj(r,o)
    return p

def inspect(path, label):
    print(f"\n===== {label}  ({path}) =====")
    with tempfile.TemporaryDirectory() as td:
        z7 = fetch_to_tmp(path, td)
        print("compressed:", os.path.getsize(z7))
        with py7zr.SevenZipFile(z7) as z:
            print("members:", z.getnames())
            z.extractall(path=td)
        for root,_,files in os.walk(td):
            for f in files:
                if f.endswith('.7z'): continue
                fp=os.path.join(root,f); sz=os.path.getsize(fp)
                with open(fp,'rb') as fh: head=fh.read(1500)
                # count lines cheaply
                with open(fp,'rb') as fh:
                    nl=sum(buf.count(b'\n') for buf in iter(lambda: fh.read(1<<20), b''))
                lines=head.decode('utf-8','replace').splitlines()
                print(f"  {f!r}: {sz} bytes, ~{nl} lines")
                for i,ln in enumerate(lines[:2]):
                    print(f"    L{i} ({len(ln.split(';'))} cols): {ln[:300]}")

inspect("RAIS/1985/AC1985.7z", "RAIS VINC per-UF 1985 (AC)")
inspect("RAIS/1985/ESTB1985.7z", "RAIS ESTAB 1985")
inspect("CAGED/2019/CAGEDEST_012019.7z", "CAGED legacy 01/2019")
