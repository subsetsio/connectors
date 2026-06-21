"""ANP Brazil (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis).

Mechanism: bulk_csv. Each subset is one or more direct CSV/ZIP files published
under https://www.gov.br/anp/.../dados-abertos/arquivos/. There is no API and no
incremental filter — we re-fetch the full corpus every run (stateless full
re-pull; revisions are picked up for free).

Per entity we re-scrape the category landing page and select the files whose
*normalized* path-pattern is in this entity's pattern set (constants.ENTITY_MAP).
This is robust to ANP rolling the year suffix forward (e.g. `-1990-2025` ->
`-1990-2026`) because the normalizer strips trailing year/month tokens — we never
hardcode a dated URL.

Raw is written as all-string Parquet (one column per source header, normalized to
ascii snake_case). All locale-specific typing — Brazilian comma decimals,
Portuguese month abbreviations, DD/MM/YYYY dates — happens in the SQL transforms,
which are the correctness gate.
"""

import io
import re
import csv
import struct
import zipfile
import unicodedata

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import get, transient_retry, raw_parquet_writer, NodeSpec, SqlNodeSpec
from constants import ENTITY_MAP, ENTITY_IDS

SLUG = "anp-brazil"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos"
BATCH_ROWS = 100_000

# ---------------------------------------------------------------------------
# discovery — mirror collect's grouping so download selects the same files
# ---------------------------------------------------------------------------

def _rel(href):
    return href.split("/arquivos/", 1)[1] if "/arquivos/" in href else href.rsplit("/", 1)[-1]


def _norm_pattern(rel):
    """Collapse date/period partitions to a single schema key (identical to the
    collect-stage normalizer)."""
    rel = rel.rsplit(".", 1)[0]
    parts = rel.split("/")
    fname = parts[-1]
    dirs = [p for p in parts[:-1] if not re.fullmatch(r"(?:19|20)\d{2}", p)]
    fname = re.sub(r"[-_]?(?:19|20)\d{2}(?:[-_](?:19|20)?\d{2})?$", "", fname)
    fname = re.sub(r"^(?:0?[1-9]|1[0-2])[-_]", "", fname)
    fname = re.sub(r"[-_](?:0?[1-9]|1[0-2])$", "", fname)
    fname = fname.strip("-_")
    return "/".join(dirs + ([fname] if fname else []))


@transient_retry()
def _http_bytes(url, **kw):
    resp = get(url, timeout=(10.0, 300.0), **kw)
    resp.raise_for_status()
    return resp.content


def _discover_urls(eid):
    import urllib.parse
    spec = ENTITY_MAP[eid]
    page = BASE + "/" + spec["slug"]
    wanted = set(spec["patterns"])
    html = _http_bytes(page).decode("utf-8", "replace")
    urls = []
    seen = set()
    for m in re.finditer(r'href="([^"]+?\.(?:csv|zip))"', html, re.I):
        href = urllib.parse.urljoin(page, m.group(1))
        if href in seen:
            continue
        seen.add(href)
        if _norm_pattern(_rel(href)) in wanted:
            urls.append(href)
    return sorted(urls)


# ---------------------------------------------------------------------------
# parsing — encoding/delimiter detection, zip + xlsx-in-zip handling
# ---------------------------------------------------------------------------

def _decode(raw):
    """BOM => UTF-8; otherwise UTF-8 strict then cp1252 (ANP ships both)."""
    if raw[:3] == b"\xef\xbb\xbf":
        return raw.decode("utf-8-sig", "replace")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252", "replace")


def _safe_col(name):
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^0-9a-zA-Z]+", "_", name).strip("_").lower()


def _csv_records(text):
    """Yield (safe_header, batch_rows) from CSV text, batched to BATCH_ROWS."""
    first = next((ln for ln in text.splitlines() if ln.strip()), "")
    delim = max((";", ",", "\t"), key=first.count)
    reader = csv.reader(io.StringIO(text), delimiter=delim)
    header = None
    batch = []
    for row in reader:
        if header is None:
            if not any(c.strip() for c in row):
                continue
            header = [_safe_col(c) for c in row]
            ncol = len(header)
            continue
        if not row or not any(c.strip() for c in row):
            continue
        # pad/truncate to header width
        if len(row) < ncol:
            row = row + [None] * (ncol - len(row))
        elif len(row) > ncol:
            row = row[:ncol]
        batch.append(row)
        if len(batch) >= BATCH_ROWS:
            yield header, batch
            batch = []
    if header is not None and batch:
        yield header, batch


def _iter_file_records(url):
    """Yield (safe_header, batch_rows) for every CSV payload behind a URL.
    Handles plain .csv, single/multi CSV-in-zip, and skips xlsx index members."""
    raw = _http_bytes(url)
    if url.lower().endswith(".zip"):
        zf = zipfile.ZipFile(io.BytesIO(raw))
        members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not members:
            raise RuntimeError(f"{url}: zip has no CSV members ({zf.namelist()[:5]})")
        for name in sorted(members):
            yield from _csv_records(_decode(zf.read(name)))
    else:
        yield from _csv_records(_decode(raw))


def _iter_entity_records(eid):
    urls = _discover_urls(eid)
    if not urls:
        raise RuntimeError(
            f"{SLUG}-{eid}: no files matched patterns {ENTITY_MAP[eid]['patterns']} "
            f"on {ENTITY_MAP[eid]['slug']} — landing page layout or paths changed"
        )
    for url in urls:
        yield from _iter_file_records(url)


# ---------------------------------------------------------------------------
# download node
# ---------------------------------------------------------------------------

def fetch_one(node_id):
    eid = node_id[len(SLUG) + 1:]
    gen = _iter_entity_records(eid)
    first = next(gen, None)
    if first is None:
        raise RuntimeError(f"{node_id}: source files produced zero rows")
    header, batch0 = first
    schema = pa.schema([(c, pa.string()) for c in header])

    def to_table(rows):
        cols = [[r[i] for r in rows] for i in range(len(header))]
        return pa.table([pa.array(c, type=pa.string()) for c in cols], schema=schema)

    with raw_parquet_writer(node_id, schema) as w:
        w.write_table(to_table(batch0))
        for hdr, batch in gen:
            if hdr != header:
                raise RuntimeError(f"{node_id}: header drift {hdr} != {header}")
            w.write_table(to_table(batch))


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# ---------------------------------------------------------------------------
# transforms — one published Delta table per subset (locale-aware typing)
# ---------------------------------------------------------------------------

# Brazilian numeric: strip thousands dots, comma -> decimal point.
def _num(col):
    return f"TRY_CAST(replace(replace(trim(\"{col}\"), '.', ''), ',', '.') AS DOUBLE)"


def _dim(col):
    return f'NULLIF(TRIM("{col}"), \'\') AS {col}'


# Month: Portuguese 3-letter (long-history files) OR numeric (mdpg files).
_MONTH = (
    "CASE upper(trim(\"{m}\")) "
    "WHEN 'JAN' THEN 1 WHEN 'FEV' THEN 2 WHEN 'MAR' THEN 3 WHEN 'ABR' THEN 4 "
    "WHEN 'MAI' THEN 5 WHEN 'JUN' THEN 6 WHEN 'JUL' THEN 7 WHEN 'AGO' THEN 8 "
    "WHEN 'SET' THEN 9 WHEN 'OUT' THEN 10 WHEN 'NOV' THEN 11 WHEN 'DEZ' THEN 12 "
    "ELSE TRY_CAST(trim(\"{m}\") AS INTEGER) END"
)

# Per-entity transform recipe: (kind, dims, values). kind picks the date source.
#   monthly -> make_date(ano, month("mes"), 1)
#   periodo -> "YYYY/MM"      mesano -> "MM/YYYY"      coleta -> "DD/MM/YYYY"
#   annual  -> year only (no date/month)
TRANSFORMS = {
    "ppgn-el-producao-petroleo-m3": ("monthly", ["grande_regiao", "unidade_da_federacao", "produto", "localizacao"], ["producao"]),
    "ppgn-el-producao-lgn-m3": ("monthly", ["grande_regiao", "unidade_da_federacao", "produto"], ["producao"]),
    "ppgn-el-queima-e-perda-gn-1000m3": ("monthly", ["grande_regiao", "unidade_da_federacao", "produto", "localizacao"], ["queimado"]),
    "ppgn-el-consumo-proprio-gn1000m3": ("monthly", ["grande_regiao", "unidade_da_federacao", "produto", "localizacao"], ["consumo"]),
    "ppgn-el-gn-disponivel-1000m3": ("monthly", ["grande_regiao", "unidade_da_federacao", "produto", "localizacao"], ["disponivel"]),
    "arquivos-producao-de-biocombustiveis-producao-biodiesel-m3": ("monthly", ["grande_regiao", "unidade_da_federacao", "produtor", "produto"], ["producao"]),
    "arquivos-producao-de-biocombustiveis-producao-etanol-anidro-hidratado-m3": ("monthly", ["grande_regiao", "unidade_da_federacao", "produto"], ["producao"]),
    "vdpb-vendas-derivados-petroleo-e-etanol-vendas-combustiveis-m3": ("monthly", ["grande_regiao", "unidade_da_federacao", "produto"], ["vendas"]),
    "vdpb-vcs-vendas-combustiveis-segmento-m3": ("monthly", ["unidade_da_federacao", "produto", "segmento"], ["vendas"]),
    "vdpb-vct-vendas-glp-tipo-vasilhame-m3": ("monthly", ["grande_regiao", "unidade_da_federacao", "vasilhame"], ["vendas"]),
    "vdpb-vendas-por-produtor-vendas-oleo-diesel-produtores-m3": ("monthly", ["derivado", "regiao", "estado"], ["vendas"]),
    "ie-petroleo-importacoes-exportacoes-petroleo": ("monthly", ["produto", "operacao_comercial"], ["importado_exportado", "dispendio_receita"]),
    "ie-gn-importacao-gas-natural": ("monthly", ["produto", "operacao_comercial"], ["importado", "dispendio"]),
    "ie-derivados-importacoes-exportacoes-derivados": ("monthly", ["produto", "operacao_comercial"], ["importado_exportado", "dispendio_receita"]),
    "mdpg-asfalto": ("monthly", ["agente_regulado", "codigo_do_produto", "nome_do_produto", "regiao_origem", "regiao_destinatario", "mercado_destinatario"], ["quantidade_de_produto_mil_ton"]),
    "mdpg-aviacao": ("monthly", ["distribuidor", "codigo_do_produto", "nome_do_produto", "regiao"], ["quantidade_de_produto_mil_m3"]),
    "mdpg-liquidos": ("monthly", ["fornecedor", "codigo_do_produto", "nome_do_produto", "regiao"], ["quantidade_de_produto_mil_m3"]),
    "mdpg-glp": ("monthly", ["distribuidor", "codigo_do_produto", "nome_do_produto", "regiao", "codigo_de_embalagem_glp"], ["quantidade_de_produto_mil_ton"]),
    "mdpg-solvente": ("monthly", ["agente_regulado", "codigo_do_produto", "nome_do_produto", "regiao_origem", "regiao_destinatario", "mercado_destinatario"], ["quantidade_de_produto_mil_m3"]),
    "mdpg-trr": ("monthly", ["agente_regulado", "codigo_do_produto", "nome_do_produto", "regiao_de_origem", "uf_origem", "regiao_de_destino", "uf_destino", "mercado_destinatario"], ["quantidade_de_produto_mil_m3"]),
    "mdpg-fornecedores-vendas-diretas": ("monthly", ["codigo_operacao", "nome_operacao", "codigo_do_produto", "nome_do_produto", "codigo_agente_regulado", "agente_regulado", "regiao_origem", "regiao_destinatario", "mercado_destinatario"], ["quantidade_de_produto_mil_m3"]),
    "mdpg-lubrificante": ("monthly", ["codigo_do_produto", "descricao_do_produto", "regiao_de_origem", "uf_de_origem", "regiao_do_destinatario", "uf_do_destinatario"], ["volume_l"]),
    "mdpg-movimentacaologistica": ("periodo", ["uf_origem", "uf_destino", "produto", "classificacao", "sub_classificacao", "operacao", "modal"], ["qtd_produto_liquido"]),
    "vdpb-vendas-de-biodiesel-vendas-biodiesel-b100-m3": ("mesano", ["regiao_origem", "regiao_destino"], ["vendas_de_biodiesel"]),
    "shpc-dsas-ca-ca": ("coleta", ["regiao_sigla", "estado_sigla", "municipio", "revenda", "cnpj_da_revenda", "nome_da_rua", "numero_rua", "complemento", "bairro", "cep", "produto", "unidade_de_medida", "bandeira"], ["valor_de_venda", "valor_de_compra"]),
    "vdpb-vaehdpm-asfalto-vendas-anuais-de-asfalto-por-municipio": ("annual", ["grande_regiao", "uf", "produto", "codigo_ibge", "municipio"], ["vendas"]),
    "vdpb-vaehdpm-glp-vendas-anuais-de-glp-por-municipio": ("annual", ["grande_regiao", "uf", "produto", "codigo_ibge", "municipio"], ["p13", "outros"]),
    "vdpb-vaehdpm-oleo-combustivel-vendas-anuais-de-oleo-combustivel-por-municipio": ("annual", ["grande_regiao", "uf", "produto", "codigo_ibge", "municipio"], ["vendas"]),
    "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado-ve": ("annual", ["grande_regiao", "estado", "produto"], ["vendas"]),
}


def _date_expr(kind):
    if kind == "monthly":
        return f'make_date(TRY_CAST(trim("ano") AS INTEGER), {_MONTH.format(m="mes")}, 1)'
    if kind == "periodo":
        return ("make_date(TRY_CAST(split_part(trim(\"periodo\"), '/', 1) AS INTEGER), "
                "TRY_CAST(split_part(trim(\"periodo\"), '/', 2) AS INTEGER), 1)")
    if kind == "mesano":
        return ("make_date(TRY_CAST(split_part(trim(\"mes_ano\"), '/', 2) AS INTEGER), "
                "TRY_CAST(split_part(trim(\"mes_ano\"), '/', 1) AS INTEGER), 1)")
    if kind == "coleta":
        return "TRY_CAST(try_strptime(trim(\"data_da_coleta\"), '%d/%m/%Y') AS DATE)"
    raise ValueError(kind)


def _build_sql(asset, kind, dims, values):
    dim_sel = ", ".join(_dim(d) for d in dims)
    val_sel = ", ".join(f"{_num(v)} AS {v}" for v in values)
    val_not_null = " OR ".join(f"{v} IS NOT NULL" for v in values)
    if kind == "annual":
        inner = (
            f'SELECT TRY_CAST(trim("ano") AS INTEGER) AS year, '
            f'{dim_sel}, {val_sel} FROM "{asset}"'
        )
        return (
            f"SELECT year, {', '.join(dims)}, {', '.join(values)} "
            f"FROM ({inner}) WHERE year IS NOT NULL AND ({val_not_null})"
        )
    inner = (
        f"SELECT {_date_expr(kind)} AS date, {dim_sel}, {val_sel} FROM \"{asset}\""
    )
    return (
        f"SELECT date, CAST(EXTRACT(year FROM date) AS INTEGER) AS year, "
        f"CAST(EXTRACT(month FROM date) AS INTEGER) AS month, "
        f"{', '.join(dims)}, {', '.join(values)} "
        f"FROM ({inner}) WHERE date IS NOT NULL AND ({val_not_null})"
    )


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-{eid}-transform",
        deps=[f"{SLUG}-{eid}"],
        sql=_build_sql(f"{SLUG}-{eid}", *TRANSFORMS[eid]),
    )
    for eid in ENTITY_IDS
]
