from subsets_utils import get
def head(url):
    raw=get(url, headers={"Range":"bytes=0-4096"}, timeout=(10,60)).content
    print("URL", url.rsplit('/',1)[-1])
    print("  first bytes:", raw[:4])
    print("  bom?", raw[:3]==b'\xef\xbb\xbf')
    # try utf-8 strict on first line
    nl=raw.find(b'\n')
    line=raw[:nl]
    for enc in ("utf-8-sig","cp1252"):
        try: print(f"  {enc}: {line.decode(enc)!r}")
        except Exception as e: print(f"  {enc}: ERR {e}")
B="https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos"
head(B+"/ie/derivados/importacoes-exportacoes-derivados-2000-2025.csv")
head(B+"/ie/etanol/importacoes-exportacoes-etanol-2012-2025.csv")
head(B+"/vdpb/vaehdpm/oleo-combustivel/vendas-anuais-de-oleo-combustivel-por-municipio.csv")
head(B+"/mdpg/lubrificante.zip")
