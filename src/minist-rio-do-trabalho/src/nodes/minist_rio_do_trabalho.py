"""Ministério do Trabalho (Brazil) — PDET labour microdata.

Source: the PDET programme (Programa de Disseminação das Estatísticas do
Trabalho) publishes de-identified administrative labour microdata over an
anonymous FTP tree at ftp://ftp.mtps.gov.br/pdet/microdados/. Each subset is a
distinct-schema *product*; period (year / yyyymm) and region/UF are partition
coordinates that become row values, not separate subsets.

Access is plain FTP — there is no HTTP/`subsets_utils.get` path for this host,
so the fetch helpers below use `urllib.request` for the ftp:// scheme
deliberately (the "route HTTP through subsets_utils" rule is about HTTP; FTP has
no library equivalent). FTP calls are wrapped in a tenacity transient retry.

Shape — **batched immutable archives** (incremental-by-immutable-batch): every
period/region archive is fetched once and never changes. Each entity's fetch fn
discovers all archives for its product from the live FTP tree (no hardcoded year
ranges), then processes each as one batch: stream the .7z to a temp file,
extract the inner `;`-delimited TXT, detect its encoding (modern Novo CAGED is
UTF-8; older RAIS/CAGED are Latin-1), and stream rows to a per-batch
`ndjson.gz` raw asset. State records which batch keys are done so a re-triggered
run resumes instead of re-fetching; raw is written before state every batch.

Columns drift across decades (1985 RAIS ≠ 2023 RAIS) so raw is NDJSON with
slugified column names — DuckDB's `read_json_auto` unions by name across batches
automatically, filling nulls. The injected `ano` / `competencia` /
`arquivo_fonte` columns carry the period & source-file dimensions the TXT itself
often omits (RAIS files have no year column).
"""

from __future__ import annotations

import io
import json
import os
import re
import shutil
import socket
import subprocess
import tempfile
import unicodedata
import urllib.error
import urllib.request
from urllib.parse import quote

import py7zr
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, load_state, raw_writer, save_state

STATE_VERSION = 1
FTP_ROOT = "ftp://ftp.mtps.gov.br/pdet/microdados/"

# FTP transport errors that warrant a retry (network blips, server-temp).
_FTP_TRANSIENT = (
    socket.timeout,
    urllib.error.URLError,
    ConnectionError,
    EOFError,
    TimeoutError,
    OSError,
    subprocess.CalledProcessError,
)


def _ftp_retry(fn):
    return retry(
        retry=retry_if_exception_type(_FTP_TRANSIENT),
        stop=stop_after_attempt(6),
        wait=wait_exponential(multiplier=2, min=2, max=120),
        reraise=True,
    )(fn)


@_ftp_retry
def _ftp_list(url: str) -> tuple[list[str], list[str]]:
    """List one FTP directory. Returns (subdir_names, file_names).

    The server emits a Windows-style listing:
        "MM-DD-YY  HH:MMAM       <DIR>          NOVO CAGED"
        "MM-DD-YY  HH:MMAM            77037 COMUNICADO_microdados.pdf"
    """
    raw = subprocess.check_output(
        [
            "curl",
            "--fail",
            "--silent",
            "--show-error",
            "--connect-timeout",
            "60",
            "--max-time",
            "300",
            url,
        ],
        stderr=subprocess.STDOUT,
    ).decode("latin-1", "replace")
    dirs: list[str] = []
    files: list[str] = []
    for line in raw.splitlines():
        line = line.rstrip("\r")
        if not line.strip():
            continue
        parts = line.split(None, 3)  # date, time, (size|<DIR>), name(+rest)
        if len(parts) < 4:
            continue
        tag, name = parts[2], parts[3].strip()
        if not name or name in (".", ".."):
            continue
        if tag == "<DIR>":
            dirs.append(name)
        else:
            files.append(name)
    return dirs, files


@_ftp_retry
def _ftp_download(url: str, dest: str) -> None:
    """Stream an FTP file to a local path.

    `urllib` handles directory listings well enough, but file responses from
    this FTP server can hang or truncate on close. Use curl for payloads; it
    has mature FTP transfer handling and returns non-zero on incomplete files.
    """
    subprocess.run(
        [
            "curl",
            "--fail",
            "--location",
            "--silent",
            "--show-error",
            "--retry",
            "5",
            "--retry-delay",
            "2",
            "--connect-timeout",
            "60",
            "--max-time",
            "3600",
            "--output",
            dest,
            url,
        ],
        check=True,
    )


def _walk_files(url: str, depth: int) -> list[tuple[str, str]]:
    """Recursively collect (dir_url, filename) up to `depth` nested levels.
    Skips legacy/parcial side-trees to keep a product's schema coherent."""
    dirs, files = _ftp_list(url)
    out = [(url, f) for f in files]
    if depth > 0:
        for d in dirs:
            if d.lower() in ("legado", "rds") or "parcial" in d.lower():
                continue
            out += _walk_files(url + quote(d) + "/", depth - 1)
    return out


def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "_", s.lower().strip()).strip("_")
    return s or "col"


def _dedup(cols: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out = []
    for i, c in enumerate(cols):
        c = c or f"col_{i}"
        if c in seen:
            seen[c] += 1
            c = f"{c}_{seen[c]}"
        else:
            seen[c] = 1
        out.append(c)
    return out


def _detect_encoding(path: str) -> str:
    """UTF-8 if the head decodes cleanly (ignoring a multibyte char clipped at
    the sample boundary), else Latin-1 — the two encodings PDET ships."""
    with open(path, "rb") as fh:
        sample = fh.read(1 << 16)
    try:
        sample.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError as e:
        return "utf-8" if e.start >= len(sample) - 3 else "latin-1"


def _iter_rows(path: str, encoding: str, extra: dict):
    """Yield one dict per data line: injected `extra` + slugified header cols.
    All values are strings; the transform casts what it needs."""
    with open(path, "r", encoding=encoding, errors="replace", newline="") as fh:
        header = fh.readline()
        if not header:
            return
        cols = _dedup([_slug(c) for c in header.rstrip("\r\n").split(";")])
        ncol = len(cols)
        for line in fh:
            line = line.rstrip("\r\n")
            if not line:
                continue
            vals = line.split(";")
            row = dict(extra)
            for i in range(ncol):
                row[cols[i]] = vals[i].strip() if i < len(vals) else None
            yield row


def _process_archive(file_url: str, asset: str, extra: dict) -> int:
    """Fetch one .7z, extract its TXT(s), stream rows to a `ndjson.gz` raw
    asset. Returns the row count written."""
    with tempfile.TemporaryDirectory() as td:
        z7 = os.path.join(td, "archive.7z")
        _ftp_download(file_url, z7)
        with open(z7, "rb") as fh:
            magic = fh.read(6)
        if magic != b"7z\xbc\xaf'\x1c":
            raise RuntimeError(f"{file_url}: downloaded payload is not a 7z archive (magic={magic.hex()})")
        try:
            with py7zr.SevenZipFile(z7) as z:
                z.extractall(path=td)
        except Exception as e:
            raise RuntimeError(f"{file_url}: failed to extract 7z archive") from e
        os.remove(z7)  # free disk before streaming the (large) TXT
        txts = [
            os.path.join(root, f)
            for root, _, files in os.walk(td)
            for f in files
            if f.lower().endswith(".txt")
        ]
        n = 0
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip", encoding="utf-8") as out:
            for tp in txts:
                enc = _detect_encoding(tp)
                for row in _iter_rows(tp, enc, extra):
                    out.write(json.dumps(row, ensure_ascii=False))
                    out.write("\n")
                    n += 1
        if n == 0:
            print(f"  [warn] {asset}: 0 rows extracted from {file_url}")
        return n


def _run_entity(node_id: str, batches: list[tuple[str, str, dict]]) -> None:
    """Process every (batch_key, file_url, extra), skipping batch keys already
    recorded done. Raw is written before state on each batch so an interrupted
    re-triggered run resumes safely."""
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "done": []}
    done = set(state.get("done", []))
    if not batches:
        raise AssertionError(f"{node_id}: discovery found 0 archives — FTP layout changed?")
    for batch_key, file_url, extra in batches:
        if batch_key in done:
            continue
        print(f"  fetching {node_id} batch {batch_key}: {file_url}", flush=True)
        asset = f"{node_id}-{batch_key}"
        _process_archive(file_url, asset, extra)
        done.add(batch_key)
        state["done"] = sorted(done)
        save_state(node_id, state)


# --- discovery -------------------------------------------------------------

def _discover_rais() -> tuple[list, list]:
    """Returns (establishment batches, worker/vínculo batches) for the RAIS
    product. Year layout differs across eras (per-UF AC1985.7z vs per-region
    RAIS_VINC_PUB_SP.7z); establishments match ESTB/ESTAB, workers are the rest."""
    base = FTP_ROOT + "RAIS/"
    dirs, _ = _ftp_list(base)
    estab, vinc = [], []
    for d in dirs:
        if not re.fullmatch(r"\d{4}", d):  # skip "2023 Parcial", "Legado"
            continue
        year = int(d)
        yurl = base + quote(d) + "/"
        _, files = _ftp_list(yurl)
        for f in files:
            if not f.lower().endswith(".7z"):
                continue
            stem = f[:-3]
            url = yurl + quote(f)
            extra = {"ano": year, "arquivo_fonte": stem}
            bk = f"{year}-{_slug(stem)}"
            low = f.lower()
            if "estb" in low or "estab" in low:
                estab.append((bk, url, extra))
            else:
                vinc.append((bk, url, extra))
    return estab, vinc


def _discover_domestica() -> list:
    base = FTP_ROOT + "TRABALHO_DOMESTICO/"
    _, files = _ftp_list(base)
    out = []
    for f in files:
        m = re.search(r"RAIS_DOM_PUB_(\d{4})", f, re.I)
        if f.lower().endswith(".7z") and m:
            year = int(m.group(1))
            out.append((f"{year}", base + quote(f), {"ano": year, "arquivo_fonte": f[:-3]}))
    return out


def _discover_caged_legacy() -> list:
    base = FTP_ROOT + "CAGED/"
    dirs, _ = _ftp_list(base)
    out = []
    for d in dirs:
        if not re.fullmatch(r"\d{4}", d):  # skip "EEC"
            continue
        yurl = base + quote(d) + "/"
        _, files = _ftp_list(yurl)
        for f in files:
            m = re.match(r"CAGEDEST_(\d{2})(\d{4})\.7z$", f, re.I)
            if m:
                comp = int(m.group(2) + m.group(1))  # yyyymm
                out.append((f"{comp}", yurl + quote(f), {"competencia": comp, "arquivo_fonte": f[:-3]}))
    return out


def _discover_caged_ajustes() -> list:
    """Out-of-deadline CAGED adjustments (CAGED_AJUSTES). Two filename eras under
    /CAGED_AJUSTES/<dir>/: monthly CAGEDEST_AJUSTES_MMYYYY.7z (2010-2020) and
    annual CAGEDEST_AJUSTES_YYYY.7z (grouped in the 2002a2009 dir). Monthly files
    inject `competencia` (yyyymm); annual aggregates inject `ano` — batch keys
    (6-digit yyyymm vs 4-digit year) never collide."""
    base = FTP_ROOT + "CAGED_AJUSTES/"
    dirs, _ = _ftp_list(base)
    out = []
    for d in dirs:
        yurl = base + quote(d) + "/"
        _, files = _ftp_list(yurl)
        for f in files:
            if not f.lower().endswith(".7z"):
                continue
            stem = f[:-3]
            m_month = re.match(r"CAGEDEST_AJUSTES_(\d{2})(\d{4})\.7z$", f, re.I)
            m_year = re.match(r"CAGEDEST_AJUSTES_(\d{4})\.7z$", f, re.I)
            if m_month:
                comp = int(m_month.group(2) + m_month.group(1))  # yyyymm
                out.append((f"{comp}", yurl + quote(f), {"competencia": comp, "arquivo_fonte": stem}))
            elif m_year:
                year = int(m_year.group(1))
                out.append((f"{year}", yurl + quote(f), {"ano": year, "arquivo_fonte": stem}))
    return out


def _discover_novo() -> dict:
    base = FTP_ROOT + quote("NOVO CAGED") + "/"
    mov, fora, exc = [], [], []
    for url, f in _walk_files(base, 2):
        m = re.match(r"CAGED(MOV|FOR|EXC)(\d{6})\.7z$", f, re.I)
        if not m:
            continue
        comp = int(m.group(2))
        bucket = {"MOV": mov, "FOR": fora, "EXC": exc}[m.group(1).upper()]
        bucket.append((f"{comp}", url + quote(f), {"competencia": comp, "arquivo_fonte": f[:-3]}))
    return {"mov": mov, "fora": fora, "exc": exc}


# --- fetch fns (one param; the runtime calls fn(spec.id)) ------------------

def fetch_rais_estabelecimentos(node_id: str) -> None:
    estab, _ = _discover_rais()
    _run_entity(node_id, estab)


def fetch_rais_domestica(node_id: str) -> None:
    _run_entity(node_id, _discover_domestica())


def fetch_caged_estatistico(node_id: str) -> None:
    _run_entity(node_id, _discover_caged_legacy())


def fetch_caged_ajustes(node_id: str) -> None:
    _run_entity(node_id, _discover_caged_ajustes())


def fetch_novo_caged_movimentacoes(node_id: str) -> None:
    _run_entity(node_id, _discover_novo()["mov"])


def fetch_novo_caged_fora_prazo(node_id: str) -> None:
    _run_entity(node_id, _discover_novo()["fora"])


def fetch_novo_caged_exclusoes(node_id: str) -> None:
    _run_entity(node_id, _discover_novo()["exc"])


DOWNLOAD_SPECS = [
    NodeSpec(id="minist-rio-do-trabalho-rais-estabelecimentos", fn=fetch_rais_estabelecimentos, kind="download"),
    NodeSpec(id="minist-rio-do-trabalho-rais-domestica", fn=fetch_rais_domestica, kind="download"),
    NodeSpec(id="minist-rio-do-trabalho-caged-estatistico", fn=fetch_caged_estatistico, kind="download"),
    NodeSpec(id="minist-rio-do-trabalho-caged-ajustes", fn=fetch_caged_ajustes, kind="download"),
    NodeSpec(id="minist-rio-do-trabalho-novo-caged-movimentacoes", fn=fetch_novo_caged_movimentacoes, kind="download"),
    NodeSpec(id="minist-rio-do-trabalho-novo-caged-fora-prazo", fn=fetch_novo_caged_fora_prazo, kind="download"),
    NodeSpec(id="minist-rio-do-trabalho-novo-caged-exclusoes", fn=fetch_novo_caged_exclusoes, kind="download"),
]
