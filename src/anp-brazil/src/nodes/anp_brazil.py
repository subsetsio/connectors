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
import os
import re
import csv
import time
import zipfile
import tempfile
import itertools
import unicodedata

import httpx
import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import (
    get, get_client, transient_retry, is_transient,
    raw_parquet_writer, NodeSpec, SqlNodeSpec,
)
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
# member curation — several mdpg categories ship one ZIP bundling *different*
# tables (Vendas vs Entregas vs Importacao; by Distribuidor/Fornecedor/Produtor;
# region-level vs UF-level; Atual vs Historico). Concatenating them blindly
# conflates distinct measures and double-counts the current period. For those
# entities we keep exactly one coherent full-history series, identified by a
# substring filter on the member basename. Entities not listed here take every
# CSV member/file (their files are already homogeneous).
# ---------------------------------------------------------------------------

MEMBER_RULES = {
    # canonical: sales by distributor, region-level, Atual + Historico (drop UF).
    "mdpg-asfalto": {"include": ["vendas_distribuidor"], "exclude": ["uf"]},
    "mdpg-solvente": {"include": ["vendas_dist"], "exclude": ["uf"]},
    "mdpg-trr": {"include": ["vendas_dist"], "exclude": ["uf"]},
    # aviacao/glp/liquidos: the "Vendas" series (agente_regulado) is the only one
    # carried across Atual + Historico; drop Entregas / UF / Importacao variants.
    "mdpg-aviacao": {"include": ["vendas"], "exclude": ["uf", "entregas"]},
    "mdpg-glp": {"include": ["vendas"], "exclude": ["uf", "entregas"]},
    "mdpg-liquidos": {"include": ["vendas"], "exclude": ["uf", "entregas", "importacao"]},
    # lubrificante bundles 10 unrelated annexes; Anexo A is the produced-volume
    # movement table the transform targets.
    "mdpg-lubrificante": {"include": ["anexo_a"], "exclude": []},
    # logistica bundles 3 distinct reports; "01" is national fuel supply.
    "mdpg-movimentacaologistica": {"include": ["logistica 01"], "exclude": []},
}


def _select_members(eid, names):
    """CSV members of a zip, narrowed by this entity's MEMBER_RULES (if any)."""
    csvs = [n for n in names if n.lower().endswith(".csv")]
    rule = MEMBER_RULES.get(eid)
    if not rule:
        return sorted(csvs)
    inc, exc = rule.get("include", []), rule.get("exclude", [])
    out = []
    for n in csvs:
        base = n.rsplit("/", 1)[-1].lower()
        if inc and not any(s in base for s in inc):
            continue
        if any(s in base for s in exc):
            continue
        out.append(n)
    return sorted(out)


# ---------------------------------------------------------------------------
# parsing — encoding/delimiter detection, headerless detection
# ---------------------------------------------------------------------------

def _decode(raw):
    """BOM => UTF-8; otherwise UTF-8 strict then cp1252 (ANP ships both)."""
    if raw[:3] == b"\xef\xbb\xbf":
        return raw.decode("utf-8-sig", "replace")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252", "replace")


def _detect_encoding(path):
    with open(path, "rb") as f:
        head = f.read(65536)
    if head[:3] == b"\xef\xbb\xbf":
        return "utf-8-sig"
    try:
        head.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "cp1252"


def _safe_col(name):
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^0-9a-zA-Z]+", "_", name).strip("_").lower()


def _pick_delim(line):
    return max((";", ",", "\t"), key=line.count)


def _looks_like_header(cells):
    """ANP headers lead with a label (ano/periodo/regiao_sigla...). A first cell
    that is purely numeric means the file shipped headerless (first row is data,
    e.g. Liquidos_Vendas_Historico_2007_a_2017.csv) — skip it rather than mint
    column names like '2007' / '1' from a data row."""
    first = next((c for c in cells if c.strip()), "")
    return bool(first) and not re.fullmatch(r"\d+", first.strip())


def _csv_batches(line_iter):
    """Yield (safe_header, batch_rows) from an iterable of CSV lines, batched to
    BATCH_ROWS. Yields nothing for an empty or headerless file."""
    it = iter(line_iter)
    pending = []
    first = None
    for raw in it:
        pending.append(raw)
        if raw.strip():
            first = raw
            break
    if first is None:
        return
    reader = csv.reader(itertools.chain(pending, it), delimiter=_pick_delim(first))
    header = None
    ncol = 0
    batch = []
    for row in reader:
        if header is None:
            if not any(c.strip() for c in row):
                continue
            if not _looks_like_header(row):
                return
            header = [_safe_col(c) for c in row]
            ncol = len(header)
            continue
        if not row or not any(c.strip() for c in row):
            continue
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


# ---------------------------------------------------------------------------
# robust download — ANP serves multi-hundred-MB files it frequently closes
# mid-body. A plain retried GET restarts from byte 0 and hits the same wall, so
# we stream to disk and resume the unfinished byte range.
# ---------------------------------------------------------------------------

def _download_to(url, dest):
    start = 0
    last = None
    for attempt in range(20):
        headers = {"Range": f"bytes={start}-"} if start else {}
        try:
            with get_client().stream(
                "GET", url, headers=headers,
                timeout=httpx.Timeout(600.0, connect=10.0),
            ) as r:
                r.raise_for_status()
                append = start > 0 and r.status_code == 206
                if not append:
                    start = 0
                with open(dest, "ab" if append else "wb") as f:
                    for chunk in r.iter_bytes(1 << 20):
                        f.write(chunk)
            return dest
        except Exception as e:  # noqa: BLE001
            if not is_transient(e):
                raise
            last = e
            start = os.path.getsize(dest) if os.path.exists(dest) else 0
            time.sleep(min(2 ** min(attempt, 6), 60))
    raise RuntimeError(f"{url}: download incomplete after retries: {last}")


@transient_retry()
def _peek_header(url):
    """Read just enough of a remote CSV to recover its header (cheap, via Range).
    Returns the safe-snake header, or None if the file is headerless/empty."""
    buf = b""
    with get_client().stream(
        "GET", url, headers={"Range": "bytes=0-65535"},
        timeout=httpx.Timeout(120.0, connect=10.0),
    ) as r:
        r.raise_for_status()
        for chunk in r.iter_bytes(16384):
            buf += chunk
            if len(buf) >= 65536:
                break
    for raw in _decode(buf).splitlines():
        if raw.strip():
            cells = next(csv.reader([raw], delimiter=_pick_delim(raw)))
            if not _looks_like_header(cells):
                return None
            return [_safe_col(c) for c in cells]
    return None


# ---------------------------------------------------------------------------
# download node — union heterogeneous files by column NAME (ANP changes a
# subset's schema across periods: adds UF columns, renames, drops a breakdown),
# so a single asset carries the superset of columns with NULLs where a file
# lacks one. zips download once and are read per member; plain CSVs are streamed
# to a tempfile one at a time (bounded disk for the 200+ shpc files).
# ---------------------------------------------------------------------------

def _zip_member_header(zip_path, member):
    with zipfile.ZipFile(zip_path) as zf:
        text = _decode(zf.read(member)[:65536])
    for raw in text.splitlines():
        if raw.strip():
            cells = next(csv.reader([raw], delimiter=_pick_delim(raw)))
            if not _looks_like_header(cells):
                return None
            return [_safe_col(c) for c in cells]
    return None


def fetch_one(node_id):
    eid = node_id[len(SLUG) + 1:]
    urls = _discover_urls(eid)
    if not urls:
        raise RuntimeError(
            f"{SLUG}-{eid}: no files matched patterns {ENTITY_MAP[eid]['patterns']} "
            f"on {ENTITY_MAP[eid]['slug']} — landing page layout or paths changed"
        )

    tmpdir = tempfile.mkdtemp(prefix=f"{eid}-")
    try:
        # Enumerate members. zips are fetched up front (one per mdpg entity,
        # modest size) and read per member; plain CSV urls stay lazy.
        members = []
        for i, url in enumerate(urls):
            if url.lower().endswith(".zip"):
                local = os.path.join(tmpdir, f"src{i}.zip")
                _download_to(url, local)
                with zipfile.ZipFile(local) as zf:
                    names = _select_members(eid, zf.namelist())
                if not names:
                    with zipfile.ZipFile(local) as zf:
                        listing = zf.namelist()[:8]
                    raise RuntimeError(
                        f"{node_id}: zip {url} has no member matching "
                        f"{MEMBER_RULES.get(eid)} (members={listing})"
                    )
                for nm in names:
                    members.append({"kind": "zip", "zip": local, "member": nm})
            else:
                members.append({"kind": "csv", "url": url, "idx": i})

        # Pass 1: header per member -> ordered column union (skip headerless).
        union, seen, used = [], set(), []
        for m in members:
            if m["kind"] == "zip":
                hdr = _zip_member_header(m["zip"], m["member"])
                label = m["member"]
            else:
                hdr = _peek_header(m["url"])
                label = m["url"].rsplit("/arquivos/", 1)[-1]
            if hdr is None:
                print(f"  [skip headerless] {node_id}: {label}")
                continue
            used.append(m)
            for c in hdr:
                if c not in seen:
                    seen.add(c)
                    union.append(c)
        if not used:
            raise RuntimeError(f"{node_id}: no usable files among {len(members)} member(s)")

        schema = pa.schema([(c, pa.string()) for c in union])

        def _emit(writer, hdr, batch):
            cols = []
            for c in union:
                if c in hdr:
                    p = hdr.index(c)
                    cols.append(pa.array([r[p] for r in batch], type=pa.string()))
                else:
                    cols.append(pa.array([None] * len(batch), type=pa.string()))
            writer.write_table(pa.table(cols, schema=schema))

        # Pass 2: stream rows, remapping each file's columns into the union.
        wrote = 0
        with raw_parquet_writer(node_id, schema) as w:
            for m in used:
                if m["kind"] == "zip":
                    with zipfile.ZipFile(m["zip"]) as zf:
                        text = _decode(zf.read(m["member"]))
                    for hdr, batch in _csv_batches(io.StringIO(text)):
                        _emit(w, hdr, batch)
                        wrote += len(batch)
                else:
                    local = os.path.join(tmpdir, f"m{m['idx']}.csv")
                    try:
                        _download_to(m["url"], local)
                        enc = _detect_encoding(local)
                        with open(local, "r", encoding=enc, errors="replace",
                                  newline="") as f:
                            for hdr, batch in _csv_batches(f):
                                _emit(w, hdr, batch)
                                wrote += len(batch)
                    finally:
                        if os.path.exists(local):
                            os.remove(local)
            if wrote == 0:
                raise RuntimeError(f"{node_id}: source files produced zero rows")
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)


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
