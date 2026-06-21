from subsets_utils import get
import io, zipfile, struct, zlib

def fetch(url, limit=None):
    h={}
    if limit: h["Range"]=f"bytes=0-{limit-1}"
    r=get(url, headers=h, timeout=(10,120))
    return r

def decode(raw):
    t=raw.decode("utf-8-sig","replace")
    if "�" in t: t=raw.decode("cp1252","replace")
    return t

def show_csv(url, n=3):
    raw=fetch(url, limit=8192).content
    t=decode(raw)
    lines=[l for l in t.splitlines() if l.strip()][:n]
    print("URL:", url.rsplit("/",1)[-1])
    for l in lines: print("   ", l[:200])

def show_zip(url, n=3):
    raw=fetch(url, limit=262144).content
    # full size
    head=get(url, headers={"Range":"bytes=0-0"}, timeout=(10,60))
    cr=head.headers.get("content-range","?")
    print("ZIP:", url.rsplit("/",1)[-1], "content-range:", cr)
    if raw[:4]!=b"PK\x03\x04":
        print("   not a zip local header"); return
    method=struct.unpack("<H",raw[8:10])[0]; fnlen=struct.unpack("<H",raw[26:28])[0]; exlen=struct.unpack("<H",raw[28:30])[0]
    member=raw[30:30+fnlen].decode("latin-1","replace")
    print("   member:", member, "method", method)
    comp=raw[30+fnlen+exlen:]
    try:
        data=zlib.decompressobj(-15).decompress(comp)
    except Exception as e:
        data=b""; print("   inflate err", e)
    t=decode(data)
    for l in [l for l in t.splitlines() if l.strip()][:n]: print("   ", l[:200])

B="https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos"
print("== production oil =="); show_csv(B+"/ppgn-el/producao-petroleo-m3.csv")
print("== ethanol =="); show_csv(B+"/arquivos-producao-de-biocombustiveis/producao-etanol-anidro-hidratado-m3-2012-2026.csv")
print("== sales national =="); show_csv(B+"/vdpb/vendas-derivados-petroleo-e-etanol/vendas-combustiveis-m3-1990-2025.csv")
print("== sales biodiesel (comma) =="); show_csv(B+"/vdpb/vendas-de-biodiesel/vendas-biodiesel-b100-m3.csv")
print("== sales municipal asfalto =="); show_csv(B+"/vdpb/vaehdpm/asfalto/vendas-anuais-de-asfalto-por-municipio.csv")
print("== imports petroleo =="); show_csv(B+"/ie/petroleo/importacoes-exportacoes-petroleo-2000-2025.csv")
print("== mov logistica zip =="); show_zip(B+"/mdpg/movimentacaologistica.zip")
print("== mov glp zip =="); show_zip(B+"/mdpg/glp.zip")
print("== price ca zip =="); show_zip(B+"/shpc/dsas/ca/ca-2025-02.zip")
print("== price dsan csv =="); show_csv(B+"/shpc/dsan/2025/precos-diesel-gnv-01.csv")
