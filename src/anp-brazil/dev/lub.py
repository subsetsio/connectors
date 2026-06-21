from subsets_utils import get
import io, zipfile, openpyxl
raw=get("https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/mdpg/lubrificante.zip", timeout=(10,120)).content
print("bytes", len(raw))
z=zipfile.ZipFile(io.BytesIO(raw))
names=z.namelist()
print("members", names[:5], "...", "is_xlsx", any(n=='[Content_Types].xml' for n in names))
# If the zip IS an xlsx (has [Content_Types].xml), load whole bytes as workbook
if '[Content_Types].xml' in names:
    wb=openpyxl.load_workbook(io.BytesIO(raw), read_only=True)
    ws=wb[wb.sheetnames[0]]
    rows=ws.iter_rows(values_only=True)
    hdr=next(rows)
    print("sheet", wb.sheetnames[0], "header:", hdr)
    for i,r in zip(range(2),rows): print("  row:", r)
else:
    # csv-in-zip
    inner=[n for n in names if n.lower().endswith('.csv')][0]
    data=z.read(inner)
    print("inner", inner, data[:200])
