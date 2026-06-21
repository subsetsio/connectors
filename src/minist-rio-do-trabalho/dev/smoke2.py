import os, sys, tempfile, urllib.request, py7zr
sys.path.insert(0,"src"); sys.path.insert(0,"src/nodes")
import nodes.minist_rio_do_trabalho as M
with tempfile.TemporaryDirectory() as td:
    z=os.path.join(td,"a.7z")
    M._ftp_download(M.FTP_ROOT+"RAIS/1985/AC1985.7z", z)
    with py7zr.SevenZipFile(z) as zz: zz.extractall(path=td)
    txt=[os.path.join(r,f) for r,_,fs in os.walk(td) for f in fs if f.lower().endswith(".txt")][0]
    enc=M._detect_encoding(txt); print("detected encoding:", enc)
    rows=list(M._iter_rows(txt, enc, {"ano":1985,"arquivo_fonte":"AC1985"}))
    print("rows:", len(rows))
    print("clean ascii keys:", sorted(rows[0].keys())[:10])
    print("any non-ascii key?:", any(not k.isascii() for k in rows[0]))
