"""Eurobarometer helpers: catalog enumeration, Volume-A selection, workbook parsing.

Kept out of the node module because the banner-cross-tab parser dwarfs the specs.

Two upstream surfaces:

* ``data.europa.eu`` CKAN-compatible ``package_search`` — the dataset catalog.
  Enumeration MUST pass ``sort=id asc``: the default relevance sort makes pages
  overlap and silently drops records.
* ``europa.eu/eurobarometer`` ``survey/get/one`` — per-survey metadata (fieldwork
  dates, series, themes). The dataset id embeds the survey id as its leading
  ``s<digits>_`` token, which is how the two surfaces join.

The "Volume A" workbook (weighted results by question) is the only aggregated
results artefact. Its layout drifted across 30 years of publication; see
``parse_sheet`` for the invariants the parser keys on rather than fixed offsets.
"""
from __future__ import annotations

import io
import re
import zipfile

from subsets_utils import get, transient_retry

CKAN_SEARCH = "https://data.europa.eu/api/hub/search/ckan/package_search"
SURVEY_ONE = "https://europa.eu/eurobarometer/api/survey/get/one"
COMMU = "/COMMU"          # publisher.resource suffix: DG Communication
PAGE_SIZE = 100
MAX_PAGES = 60            # safety ceiling; ~1132 records at 100/page today

# The volume code lives inside the resource filename, whose spelling drifted:
#   OP_VolumeAEB764HOMEhomeaffairs_v1.zip   VolumeAFlash336DGECFIN.zip
#   VolumeASP410EB802AGRIpacEN.zip          EB86A.zip / E76A.zip
#   FL382a_Volume A_xls.zip                 OP_EB73 VOLA.zip
#   Standard Eurobarometer 104_Autumn 2025_volume A.xlsx
# Anchor on a closed vocabulary so "VolumeAEB843" reads A and "VolumeAAEB764"
# reads AA. Longest alternatives first.
_CODES = r"(AAP|AA|AP|BP|SC|A|B|C|D|S)"
_AFTER = r"(?=EB\d|FL\d|EP\d|SP\d|Flash\s*\d|E\d|_|\s|\.|\(|$)"
_VOL_RE = re.compile(r"(?:volumes?|tables?|vol)\s*_?\s*" + _CODES + _AFTER, re.I)
_LEGACY_RE = re.compile(r"\b(?:EB|E)\d+(?:\.\d+)?[._]?" + _CODES + r"\.zip", re.I)

TOC_NAMES = {"index", "content", "contents", "table of contents", "toc", "sommaire",
             "note", "notes"}
BASE_LABELS = {"TOTAL", "WEIGHTED TOTAL", "TOTAL WEIGHTED", "BASE",
               "UNWEIGHTED BASE", "WEIGHTED BASE", "TOTAL N"}
NULL_TOKENS = {"-", "", ":", "n.a.", "na", "n/a", "*", "nan", "none"}
SUBTOTAL_RE = re.compile(r"^total\s*['\"‘’]", re.I)
CODE_RE = re.compile(r"^[A-Z][A-Z0-9\-\+/]{0,11}$")
MAX_BANNER_LEN = 24
SURVEY_ID_RE = re.compile(r"^s(\d+)_", re.I)


# --------------------------------------------------------------------------
# catalog
# --------------------------------------------------------------------------

@transient_retry()
def _get_json(url, **params):
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_bytes(url):
    resp = get(url, timeout=(15.0, 300.0))
    resp.raise_for_status()
    return resp.content


def enumerate_commu_datasets():
    """Every DG-Communication Eurobarometer dataset record, deterministically paged."""
    out, start, count = {}, 0, None
    for page in range(MAX_PAGES + 1):
        if page > MAX_PAGES:
            raise RuntimeError(
                f"catalog exceeded {MAX_PAGES} pages (count={count}) — the source "
                "shape changed; refusing to crawl blindly")
        res = _get_json(CKAN_SEARCH, q="eurobarometer", rows=PAGE_SIZE,
                        start=start, sort="id asc")["result"]
        count = res["count"]
        batch = res.get("results") or []
        if not batch:
            break
        for rec in batch:
            out[rec["id"]] = rec
        start += PAGE_SIZE
        if start >= count:
            break
    if count and len(out) < count * 0.95:
        raise RuntimeError(f"enumerated {len(out)} of {count} catalog records — "
                           "pagination lost records")
    return {k: v for k, v in out.items()
            if ((v.get("publisher") or {}).get("resource") or "").endswith(COMMU)}


def resource_title(res):
    return ((res.get("translation") or {}).get("en") or {}).get("title") or ""


def volume_code(res):
    """The Volume letter this resource carries ('A', 'AA', 'C', ...) or None."""
    title = resource_title(res)
    for rx in (_VOL_RE, _LEGACY_RE):
        m = rx.search(title)
        if m:
            return m.group(1).upper()
    return None


def resource_url(res):
    """access_url arrives wrapped in literal square brackets."""
    u = res.get("access_url")
    if isinstance(u, list):
        u = u[0] if u else None
    if not u:
        return None
    return str(u).strip().lstrip("[").rstrip("]").strip() or None


def volume_a_resources(rec):
    """Every Volume-A resource of a catalog record (a few waves ship EU27 and
    EU28 restatements, or an a/b split, as separate Volume-A files)."""
    out = []
    for res in rec.get("resources") or []:
        if volume_code(res) != "A":
            continue
        url = resource_url(res)
        if url:
            out.append((resource_title(res), url))
    return sorted(out)


def dataset_title(rec):
    return ((rec.get("translation") or {}).get("en") or {}).get("title")


def dataset_notes(rec):
    return ((rec.get("translation") or {}).get("en") or {}).get("notes")


def survey_id_of(dataset_id):
    m = SURVEY_ID_RE.match(dataset_id)
    return int(m.group(1)) if m else None


def fetch_survey_metadata(survey_id):
    """Per-survey metadata from the EC portal API, or None when it has no record.

    ``survey/get/all`` was retired (404) and ``survey/search`` is a PDF document
    index; ``get/one`` is the only surface that returns clean survey metadata.
    """
    resp = get(SURVEY_ONE, params={"id": survey_id}, timeout=(10.0, 60.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    body = resp.json()
    return body if isinstance(body, dict) and body.get("id") else None


# --------------------------------------------------------------------------
# workbook reading
# --------------------------------------------------------------------------

def workbook_members(payload):
    """yield (member_name, bytes) for each workbook in a downloaded payload.

    A payload is either a bare .xls, a bare .xlsx (itself a zip), or a zip
    holding one or more workbooks. Some older waves ship a zip of .txt/.pdf/.doc
    instead — those yield nothing.
    """
    if payload[:2] != b"PK":
        yield "__xls__", payload
        return
    try:
        zf = zipfile.ZipFile(io.BytesIO(payload))
    except zipfile.BadZipFile:
        return
    names = zf.namelist()
    books = [n for n in names
             if n.lower().endswith((".xls", ".xlsx")) and not n.startswith("__MACOSX")]
    if books:
        for name in sorted(books):
            yield name, zf.read(name)
    elif "[Content_Types].xml" in names:
        yield "__xlsx__", payload          # the payload IS an xlsx


def sheets_of(data):
    """{sheet_name: [row_tuple, ...]} — xlrd for old binary .xls, openpyxl for .xlsx."""
    if data[:2] == b"PK":
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
        try:
            return {sn: [tuple(r) for r in wb[sn].iter_rows(values_only=True)]
                    for sn in wb.sheetnames}
        finally:
            wb.close()
    import xlrd
    wb = xlrd.open_workbook(file_contents=data)
    return {
        sn: [tuple(c.value if c.ctype != 0 else None for c in wb.sheet_by_name(sn).row(r))
             for r in range(wb.sheet_by_name(sn).nrows)]
        for sn in wb.sheet_names()
    }


# --------------------------------------------------------------------------
# banner cross-tab parsing
# --------------------------------------------------------------------------

def _s(v):
    return "" if v is None else str(v).strip()


def _num(v):
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    t = _s(v).replace(" ", " ").replace(",", ".").replace("%", "").strip()
    if t.lower() in NULL_TOKENS:
        return None
    try:
        return float(t)
    except ValueError:
        return None


def _is_null_token(v):
    return _s(v).lower() in NULL_TOKENS


def find_base(rows):
    """Locate the base ('TOTAL') row: (row_index, label_col, mode).

    mode is 'triplet' when answers are N / Total % / Valid % triples (Flash
    waves), otherwise 'pair' (a count row then a share row).
    """
    for i, row in enumerate(rows[:60]):
        for lab_col in (1, 0, 2):
            if lab_col >= len(row) or _s(row[lab_col]).upper() not in BASE_LABELS:
                continue
            # A real base row carries numbers in its data columns. A bare
            # "TOTAL" cell can also be a banner COLUMN header (FL176).
            if not any(_num(row[c]) is not None for c in range(lab_col + 1, len(row))):
                continue
            stats = {_s(r[lab_col]).upper() for r in rows[i + 1:i + 8] if lab_col < len(r)}
            mode = "triplet" if ("N" in stats and any(s.startswith("TOTAL %") for s in stats)) \
                else "pair"
            return i, lab_col, mode
    return None


def _banner_token(v):
    """Header cells are bilingual ('UE28\\nEU28' -> 'EU28') or multi-line labels
    ('Day 1\\n28 Dec.'). Keep the last line only when it reads as a code."""
    raw = _s(v)
    if not raw:
        return None
    lines = [x.strip() for x in raw.split("\n") if x.strip()]
    if not lines:
        return None
    tok = lines[-1] if CODE_RE.match(lines[-1]) else " ".join(lines)
    tok = re.sub(r"\s+", " ", tok).strip(" .:")
    if not tok or len(tok) > MAX_BANNER_LEN:
        return None
    if tok.upper() in BASE_LABELS or tok.lower() in NULL_TOKENS:
        return None
    return tok


def banner_columns(rows, base_idx, data_start):
    """{column_index: banner_label} from the nearest labelled row above the base.

    Banner columns are usually countries / EU aggregates, but a few waves break
    results out by fieldwork day or country group instead — accept any short label.
    """
    for i in range(base_idx - 1, -1, -1):
        row = rows[i]
        if len(row) <= data_start or not any(_s(row[c]) for c in range(data_start, len(row))):
            continue
        out = {c: _banner_token(row[c]) for c in range(data_start, len(row))}
        return {c: t for c, t in out.items() if t}
    return {}


def _share_scale(values):
    """Shares are stored as fractions in most waves and as percents in others."""
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    top = max(vals)
    if top <= 1.0001:
        return 1.0
    if top <= 100.5:
        return 100.0
    return None


def parse_sheet(rows):
    """One question sheet -> list of row dicts, or None when it is not a banner.

    Layout invariants (asserted, never fixed offsets):
      * a base row whose label cell reads TOTAL / Weighted total and whose data
        cells are numeric — the weighted N per banner column;
      * the nearest labelled row above it names the banner columns;
      * below it, answers repeat as FR/EN row pairs (count row, share row) or,
        on Flash waves, as N / Total % / Valid % triples.
    """
    hit = find_base(rows)
    if not hit:
        return None
    base_idx, lab_col, mode = hit
    data_start = lab_col + 1
    banners = banner_columns(rows, base_idx, data_start)
    if not banners:
        return None
    cols = sorted(banners)
    base_row = rows[base_idx]
    base_n = {c: (_num(base_row[c]) if c < len(base_row) else None) for c in cols}

    body = [r for r in rows[base_idx + 1:] if any(_s(x) for x in r)]
    step = 3 if mode == "triplet" else 2
    out, answer_index = [], 0

    for i in range(0, len(body) - step + 1, step):
        group = body[i:i + step]
        count_row, share_row = group[0], group[1]
        if mode == "triplet":
            if lab_col >= len(count_row) or _s(count_row[lab_col]).upper() != "N":
                break
            label_fr = None
            answer = _s(count_row[lab_col - 1]) if lab_col >= 1 else ""
        else:
            label_fr = _s(count_row[lab_col]) if lab_col < len(count_row) else ""
            answer = _s(share_row[lab_col]) if lab_col < len(share_row) else ""
            answer = answer or label_fr
        if not answer:
            continue

        shares = {c: (_num(share_row[c]) if c < len(share_row) else None) for c in cols}
        scale = _share_scale(list(shares.values()))
        if scale is None:
            # An all-null share row is legitimate (every cell a '-' zero token);
            # anything else means the pairing has drifted — stop this sheet.
            if not any(_is_null_token(share_row[c]) if c < len(share_row) else False
                       for c in cols):
                break
            scale = 1.0

        subtotal = bool(SUBTOTAL_RE.match(answer)) or answer.upper() in BASE_LABELS
        for c in cols:
            weighted_n = _num(count_row[c]) if c < len(count_row) else None
            share = shares[c]
            share = None if share is None else share / scale
            if share is not None and not 0.0 <= share <= 1.0001:
                share = None      # never publish a count as if it were a fraction
            if weighted_n is None and share is None:
                continue
            label = banners[c]
            out.append({
                "banner": label,
                "country": label if CODE_RE.match(label) else None,
                "answer": answer,
                "answer_fr": label_fr or None,
                "answer_index": answer_index,
                "is_subtotal": subtotal,
                "weighted_n": weighted_n,
                "share": share,
                "base_n": base_n.get(c),
            })
        answer_index += 1
    return out or None


def parse_volume_a(payload, source_file_hint):
    """Every question sheet of a Volume-A payload, as flat row dicts."""
    rows = []
    for member, data in workbook_members(payload):
        member_name = source_file_hint if member.startswith("__") else member
        try:
            sheets = sheets_of(data)
        except Exception as exc:  # a corrupt/unsupported workbook is not a bug
            print(f"    [warn] cannot open member {member!r}: {type(exc).__name__}: {exc}")
            continue
        for sheet_name, sheet_rows in sheets.items():
            if sheet_name.strip().lower() in TOC_NAMES:
                continue
            parsed = parse_sheet(sheet_rows)
            if not parsed:
                continue
            for row in parsed:
                row["question_code"] = sheet_name.strip()
                row["source_file"] = member_name
                rows.append(row)
    return rows


def download(url):
    return _get_bytes(url)
