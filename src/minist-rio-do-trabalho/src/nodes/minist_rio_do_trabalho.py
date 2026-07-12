"""Ministério do Trabalho (Brazil) — PDET labour microdata.

Source: the PDET programme (Programa de Disseminação das Estatísticas do
Trabalho) publishes de-identified administrative labour microdata over an
anonymous FTP tree at ftp://ftp.mtps.gov.br/pdet/microdados/. Each subset is a
distinct-schema *product*; period (year / yyyymm) and region/UF are partition
coordinates that become row values, not separate subsets.

Access is plain FTP — there is no HTTP/`subsets_utils.get` path for this host,
so the fetch helpers below use curl for the ftp:// scheme deliberately (the
"route HTTP through subsets_utils" rule is about HTTP; FTP has no library
equivalent). FTP calls are wrapped in a tenacity transient retry.

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
from datetime import date
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


@_ftp_retry
def _ftp_exists(url: str) -> bool:
    """Probe one expected FTP file without listing its parent directory."""
    proc = subprocess.run(
        [
            "curl",
            "--fail",
            "--silent",
            "--show-error",
            "--connect-timeout",
            "20",
            "--max-time",
            "60",
            "-I",
            url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode == 0:
        return True
    # FTP servers report missing path components as 9 and missing files as 78.
    if proc.returncode in (9, 78):
        return False
    raise subprocess.CalledProcessError(proc.returncode, proc.args, output=proc.stderr)


def _month_ints(start_year: int, start_month: int, end_year: int, end_month: int) -> list[int]:
    out = []
    year, month = start_year, start_month
    while (year, month) <= (end_year, end_month):
        out.append(year * 100 + month)
        month += 1
        if month == 13:
            year += 1
            month = 1
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


def _txt_paths(root_dir: str) -> list[str]:
    return [
        os.path.join(root, f)
        for root, _, files in os.walk(root_dir)
        for f in files
        if f.lower().endswith(".txt")
    ]


def _extract_archive(z7_path: str, out_dir: str, file_url: str) -> list[str]:
    try:
        with py7zr.SevenZipFile(z7_path) as z:
            z.extractall(path=out_dir)
    except Exception as py_error:
        txts = _txt_paths(out_dir)
        if txts:
            print(f"  [warn] {file_url}: py7zr reported {type(py_error).__name__}, using extracted TXT(s)", flush=True)
            return txts

        fallback_output = ""
        for name in ("7z", "7zz", "7za", "bsdtar"):
            exe = shutil.which(name)
            if not exe:
                continue
            if name == "bsdtar":
                args = [exe, "-xf", z7_path, "-C", out_dir]
            else:
                args = [exe, "x", "-y", f"-o{out_dir}", z7_path]
            proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            fallback_output = proc.stdout[-2000:]
            txts = _txt_paths(out_dir)
            if txts:
                if proc.returncode != 0:
                    print(f"  [warn] {file_url}: {name} exited {proc.returncode} but produced TXT(s)", flush=True)
                return txts

        raise RuntimeError(
            f"{file_url}: failed to extract 7z archive with py7zr and system fallbacks; "
            f"py7zr={type(py_error).__name__}: {py_error}; fallback_tail={fallback_output!r}"
        ) from py_error

    txts = _txt_paths(out_dir)
    if not txts:
        raise RuntimeError(f"{file_url}: extracted archive contains no TXT files")
    return txts


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
        txts = _extract_archive(z7, td, file_url)
        os.remove(z7)  # free disk before streaming the (large) TXT
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
    product. We only publish establishments here; worker/vínculo files are a
    distinct, much larger deferred entity.

    Avoid listing the FTP tree in production: the root listing intermittently
    hangs in GitHub Actions, while individual archive URLs respond quickly.
    Naming is stable: ESTBYYYY through 2017, RAIS_ESTAB_PUB from 2018 onward.
    """
    base = FTP_ROOT + "RAIS/"
    estab, vinc = [], []
    current_year = date.today().year
    for year in range(1985, current_year):
        filename = f"ESTB{year}.7z" if year <= 2017 else "RAIS_ESTAB_PUB.7z"
        yurl = base + f"{year}/"
        url = yurl + quote(filename)
        if _ftp_exists(url):
            stem = filename[:-3]
            estab.append((f"{year}-{_slug(stem)}", url, {"ano": year, "arquivo_fonte": stem}))
    return estab, vinc


def _discover_domestica() -> list:
    base = FTP_ROOT + "TRABALHO_DOMESTICO/"
    out = []
    for year in range(2015, date.today().year):
        filename = f"RAIS_DOM_PUB_{year}.7z"
        url = base + quote(filename)
        if _ftp_exists(url):
            out.append((f"{year}", url, {"ano": year, "arquivo_fonte": filename[:-3]}))
    return out


def _discover_caged_legacy() -> list:
    base = FTP_ROOT + "CAGED/"
    out = []
    for comp in _month_ints(2007, 1, 2019, 12):
        year, month = divmod(comp, 100)
        filename = f"CAGEDEST_{month:02d}{year}.7z"
        out.append((f"{comp}", base + f"{year}/" + quote(filename), {"competencia": comp, "arquivo_fonte": filename[:-3]}))
    return out


def _discover_caged_ajustes() -> list:
    """Out-of-deadline CAGED adjustments (CAGED_AJUSTES). Two filename eras under
    /CAGED_AJUSTES/<dir>/: monthly CAGEDEST_AJUSTES_MMYYYY.7z (2010-2020) and
    annual CAGEDEST_AJUSTES_YYYY.7z (grouped in the 2002a2009 dir). Monthly files
    inject `competencia` (yyyymm); annual aggregates inject `ano` — batch keys
    (6-digit yyyymm vs 4-digit year) never collide."""
    base = FTP_ROOT + "CAGED_AJUSTES/"
    out = []
    for year in range(2002, 2010):
        filename = f"CAGEDEST_AJUSTES_{year}.7z"
        out.append((f"{year}", base + "2002a2009/" + quote(filename), {"ano": year, "arquivo_fonte": filename[:-3]}))
    for comp in _month_ints(2010, 1, 2020, 12):
        year, month = divmod(comp, 100)
        filename = f"CAGEDEST_AJUSTES_{month:02d}{year}.7z"
        out.append((f"{comp}", base + f"{year}/" + quote(filename), {"competencia": comp, "arquivo_fonte": filename[:-3]}))
    return out


def _discover_novo() -> dict:
    base = FTP_ROOT + quote("NOVO CAGED") + "/"
    mov, fora, exc = [], [], []
    today = date.today()
    # Releases lag the calendar; probe month URLs through the prior month and
    # include only the files that exist.
    prior_month = today.month - 1
    prior_year = today.year
    if prior_month == 0:
        prior_year -= 1
        prior_month = 12
    for comp in _month_ints(2020, 1, prior_year, prior_month):
        year = comp // 100
        month_url = base + f"{year}/{comp}/"
        for prefix, bucket in (("MOV", mov), ("FOR", fora), ("EXC", exc)):
            filename = f"CAGED{prefix}{comp}.7z"
            url = month_url + quote(filename)
            if _ftp_exists(url):
                bucket.append((f"{comp}", url, {"competencia": comp, "arquivo_fonte": filename[:-3]}))
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
