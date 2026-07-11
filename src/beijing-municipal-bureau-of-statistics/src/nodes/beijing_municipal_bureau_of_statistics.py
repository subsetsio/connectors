"""Beijing Municipal Bureau of Statistics — Macroeconomic & Social Development
Basic Database (北京市宏观经济与社会发展基础数据库).

Access mechanism: ``macro_db_rest`` — the Struts report platform at
``hgk.tjj.beijing.gov.cn``. There is NO bulk export; data is fetched one report
table at a time. Per report the flow (all on one shared cookie jar, which the
``subsets_utils`` httpx client keeps for us) is:

  1. GET  ``.../query/queryReport/queryReportAction?method=queryHtmlStyle`` for
     the report — seeds the server-side JSESSIONID state that the data call
     requires (a cold POST returns ``[]``), and carries the report's
     ``reportVersion`` (template version) + ``sourceDepartmentCode`` in its
     ``showSinglereport`` script tag.
  2. POST ``QueryReportAction!queryRptTimeFreqMask`` -> the available time masks
     (a single year token for annual ``01`` reports whose columns span all
     history; one ``YYYY/MM`` token per period for progress ``05`` reports).
  3. POST ``QueryReportAction!updateReportHtml`` (once) -> the HTML table-style
     template that maps each opaque cell id (e.g. ``10-2_1``) to its grid
     position, from which we recover the row label (indicator) and column header.
  4. POST ``QueryReportAction!queryReportData`` per mask -> cell values, a list
     parallel to the row's ``metaData`` cell-id list.

We unflatten the pivot (template cell positions + per-mask values) into long
rows ``(report_number, mask, indicator, col_label, value)`` and persist NDJSON
(labels are free-form Chinese text — drifty, so NDJSON over parquet).

Fetch shape: stateless full re-pull (shape 1). The whole corpus is re-fetched
each run and overwritten; each report is small and there is no incremental /
``since`` filter, so a watermark would buy nothing and would silently skip
revised periods. Freshness gating is the maintain step's job.
"""
import re
import html
import json

import httpx
import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    post,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITIES

SLUG = "beijing-municipal-bureau-of-statistics"
HOST = "https://hgk.tjj.beijing.gov.cn"
VIEWER = HOST + "/query/queryReport/queryReportAction"
ACTION = HOST + "/query/queryres/queryreport/QueryReportAction!"

# spec-id -> {id, report, subject, sort}; pure computation over the imported
# constant (no I/O), so it is safe at module level.
def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


_BY_SPEC = {_spec_id(e["id"]): e for e in ENTITIES}

# These reports are present in the source catalog/viewer but currently do not
# yield publishable data through the verified REST path. They are covered by
# harness waive-spec records; keep them out of the executable DAG so the graph
# only contains tables that can publish real rows.
UNAVAILABLE_SPEC_IDS = {
    "beijing-municipal-bureau-of-statistics-01-1",
    "beijing-municipal-bureau-of-statistics-01-ls-031-001",
    "beijing-municipal-bureau-of-statistics-01-ls-031-002",
    "beijing-municipal-bureau-of-statistics-01-ls-10-01-1",
    "beijing-municipal-bureau-of-statistics-01-ls-10-02",
    "beijing-municipal-bureau-of-statistics-01-ls-10-03",
    "beijing-municipal-bureau-of-statistics-01-ls-10-04",
    "beijing-municipal-bureau-of-statistics-01-ls-10-05",
    "beijing-municipal-bureau-of-statistics-01-ls-10-06",
    "beijing-municipal-bureau-of-statistics-01-ls-10-07",
    "beijing-municipal-bureau-of-statistics-01-ls-10-08",
    "beijing-municipal-bureau-of-statistics-01-ls-11-01",
    "beijing-municipal-bureau-of-statistics-01-ls-11-02",
    "beijing-municipal-bureau-of-statistics-01-ls-11-03",
    "beijing-municipal-bureau-of-statistics-01-ls-11-04",
    "beijing-municipal-bureau-of-statistics-01-ls-11-05",
    "beijing-municipal-bureau-of-statistics-01-ls-11-06",
    "beijing-municipal-bureau-of-statistics-01-ls-11-07",
    "beijing-municipal-bureau-of-statistics-01-ls-11-08",
    "beijing-municipal-bureau-of-statistics-01-ls-11-08-1",
    "beijing-municipal-bureau-of-statistics-01-ls-11-09",
    "beijing-municipal-bureau-of-statistics-01-ls-11-10",
    "beijing-municipal-bureau-of-statistics-01-ls-11-11",
    "beijing-municipal-bureau-of-statistics-01-ls-11-12",
    "beijing-municipal-bureau-of-statistics-01-ls-11-14",
    "beijing-municipal-bureau-of-statistics-01-ls-11-15",
    "beijing-municipal-bureau-of-statistics-01-ls-12-01",
    "beijing-municipal-bureau-of-statistics-01-ls-12-01-01",
    "beijing-municipal-bureau-of-statistics-01-ls-12-01-02",
    "beijing-municipal-bureau-of-statistics-01-ls-12-04",
    "beijing-municipal-bureau-of-statistics-01-ls-12-05",
    "beijing-municipal-bureau-of-statistics-01-ls-12-06",
    "beijing-municipal-bureau-of-statistics-01-ls-12-07",
    "beijing-municipal-bureau-of-statistics-01-ls-12-09",
    "beijing-municipal-bureau-of-statistics-01-ls-12-09-1",
    "beijing-municipal-bureau-of-statistics-01-ls-12-10",
    "beijing-municipal-bureau-of-statistics-01-ls-12-11",
    "beijing-municipal-bureau-of-statistics-01-ls-12-12",
    "beijing-municipal-bureau-of-statistics-01-ls-12-13",
    "beijing-municipal-bureau-of-statistics-01-ls-12-14",
    "beijing-municipal-bureau-of-statistics-01-ls-12-15",
    "beijing-municipal-bureau-of-statistics-01-ls-12-17",
    "beijing-municipal-bureau-of-statistics-01-ls-13-01",
    "beijing-municipal-bureau-of-statistics-01-ls-13-01-1",
    "beijing-municipal-bureau-of-statistics-01-ls-13-02",
    "beijing-municipal-bureau-of-statistics-01-ls-13-03",
    "beijing-municipal-bureau-of-statistics-01-ls-13-03-1",
    "beijing-municipal-bureau-of-statistics-01-ls-14-01",
    "beijing-municipal-bureau-of-statistics-01-ls-14-02",
    "beijing-municipal-bureau-of-statistics-01-ls-14-03",
    "beijing-municipal-bureau-of-statistics-01-ls-14-04",
    "beijing-municipal-bureau-of-statistics-01-ls-14-05",
    "beijing-municipal-bureau-of-statistics-01-ls-14-06",
    "beijing-municipal-bureau-of-statistics-01-ls-15-01",
    "beijing-municipal-bureau-of-statistics-01-ls-15-02",
    "beijing-municipal-bureau-of-statistics-01-ls-15-03",
    "beijing-municipal-bureau-of-statistics-01-ls-15-03-1",
    "beijing-municipal-bureau-of-statistics-01-ls-15-04",
    "beijing-municipal-bureau-of-statistics-01-ls-15-04-1",
    "beijing-municipal-bureau-of-statistics-01-ls-15-05",
    "beijing-municipal-bureau-of-statistics-01-ls-15-05-1",
    "beijing-municipal-bureau-of-statistics-01-ls-15-06",
    "beijing-municipal-bureau-of-statistics-01-ls-15-07",
    "beijing-municipal-bureau-of-statistics-01-ls-15-08",
    "beijing-municipal-bureau-of-statistics-01-ls-15-08-1",
    "beijing-municipal-bureau-of-statistics-01-ls-15-09",
    "beijing-municipal-bureau-of-statistics-01-ls-15-09-1",
    "beijing-municipal-bureau-of-statistics-01-ls-15-09-2",
    "beijing-municipal-bureau-of-statistics-01-ls-15-10",
    "beijing-municipal-bureau-of-statistics-01-ls-16-01",
    "beijing-municipal-bureau-of-statistics-01-ls-16-06",
    "beijing-municipal-bureau-of-statistics-01-ls-16-07",
    "beijing-municipal-bureau-of-statistics-01-ls-16-08",
    "beijing-municipal-bureau-of-statistics-01-ls-16-10",
    "beijing-municipal-bureau-of-statistics-01-ls-16-11",
    "beijing-municipal-bureau-of-statistics-01-ls-16-12",
    "beijing-municipal-bureau-of-statistics-01-ls-16-13",
    "beijing-municipal-bureau-of-statistics-01-ls-16-14",
    "beijing-municipal-bureau-of-statistics-01-ls-17-01",
    "beijing-municipal-bureau-of-statistics-01-ls-17-02",
    "beijing-municipal-bureau-of-statistics-01-ls-17-03",
    "beijing-municipal-bureau-of-statistics-01-ls-17-04",
    "beijing-municipal-bureau-of-statistics-01-ls-17-05",
    "beijing-municipal-bureau-of-statistics-01-ls-17-06",
    "beijing-municipal-bureau-of-statistics-01-ls-18-01",
    "beijing-municipal-bureau-of-statistics-01-ls-18-01-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-02",
    "beijing-municipal-bureau-of-statistics-01-ls-18-02-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-03",
    "beijing-municipal-bureau-of-statistics-01-ls-18-03-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-04",
    "beijing-municipal-bureau-of-statistics-01-ls-18-04-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-05",
    "beijing-municipal-bureau-of-statistics-01-ls-18-05-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-06",
    "beijing-municipal-bureau-of-statistics-01-ls-18-06-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-07",
    "beijing-municipal-bureau-of-statistics-01-ls-18-07-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-08",
    "beijing-municipal-bureau-of-statistics-01-ls-18-08-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-09",
    "beijing-municipal-bureau-of-statistics-01-ls-18-09-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-11",
    "beijing-municipal-bureau-of-statistics-01-ls-18-12",
    "beijing-municipal-bureau-of-statistics-01-ls-18-13",
    "beijing-municipal-bureau-of-statistics-01-ls-18-13-1",
    "beijing-municipal-bureau-of-statistics-01-ls-18-14",
    "beijing-municipal-bureau-of-statistics-01-ls-18-15",
    "beijing-municipal-bureau-of-statistics-01-ls-18-16",
    "beijing-municipal-bureau-of-statistics-01-ls-18-17",
    "beijing-municipal-bureau-of-statistics-01-ls-18-18",
    "beijing-municipal-bureau-of-statistics-01-ls-18-19",
    "beijing-municipal-bureau-of-statistics-01-ls-18-20",
    "beijing-municipal-bureau-of-statistics-01-ls-18-21",
    "beijing-municipal-bureau-of-statistics-01-ls-18-22",
    "beijing-municipal-bureau-of-statistics-01-ls-18-23",
    "beijing-municipal-bureau-of-statistics-01-ls-18-25",
    "beijing-municipal-bureau-of-statistics-01-ls-18-27",
    "beijing-municipal-bureau-of-statistics-01-ls-18-28",
    "beijing-municipal-bureau-of-statistics-01-ls-18-29",
    "beijing-municipal-bureau-of-statistics-01-ls-18-30",
    "beijing-municipal-bureau-of-statistics-01-ls-18-31",
    "beijing-municipal-bureau-of-statistics-01-ls-18-32",
    "beijing-municipal-bureau-of-statistics-01-ls-18-33",
    "beijing-municipal-bureau-of-statistics-01-ls-18-34",
    "beijing-municipal-bureau-of-statistics-01-ls-18-35",
    "beijing-municipal-bureau-of-statistics-01-ls-19-01",
    "beijing-municipal-bureau-of-statistics-01-ls-19-02",
    "beijing-municipal-bureau-of-statistics-01-ls-19-03",
    "beijing-municipal-bureau-of-statistics-01-ls-19-05",
    "beijing-municipal-bureau-of-statistics-01-ls-19-08",
    "beijing-municipal-bureau-of-statistics-01-ls-19-08-1",
    "beijing-municipal-bureau-of-statistics-01-ls-19-10",
    "beijing-municipal-bureau-of-statistics-01-ls-2-01",
    "beijing-municipal-bureau-of-statistics-01-ls-2-02",
    "beijing-municipal-bureau-of-statistics-01-ls-2-03",
    "beijing-municipal-bureau-of-statistics-01-ls-2-08",
    "beijing-municipal-bureau-of-statistics-01-ls-2-09",
    "beijing-municipal-bureau-of-statistics-01-ls-2-10",
    "beijing-municipal-bureau-of-statistics-01-ls-2-11",
    "beijing-municipal-bureau-of-statistics-01-ls-2-12",
    "beijing-municipal-bureau-of-statistics-01-ls-2-13",
    "beijing-municipal-bureau-of-statistics-01-ls-2-15",
    "beijing-municipal-bureau-of-statistics-01-ls-2-16",
    "beijing-municipal-bureau-of-statistics-01-ls-2-18",
    "beijing-municipal-bureau-of-statistics-01-ls-20-02",
    "beijing-municipal-bureau-of-statistics-01-ls-21-02",
    "beijing-municipal-bureau-of-statistics-01-ls-21-03",
    "beijing-municipal-bureau-of-statistics-01-ls-21-04",
    "beijing-municipal-bureau-of-statistics-01-ls-21-05",
    "beijing-municipal-bureau-of-statistics-01-ls-21-06",
    "beijing-municipal-bureau-of-statistics-01-ls-21-07",
    "beijing-municipal-bureau-of-statistics-01-ls-21-08",
    "beijing-municipal-bureau-of-statistics-01-ls-21-10",
    "beijing-municipal-bureau-of-statistics-01-ls-21-13",
    "beijing-municipal-bureau-of-statistics-01-ls-21-14",
    "beijing-municipal-bureau-of-statistics-01-ls-21-15",
    "beijing-municipal-bureau-of-statistics-01-ls-21-17",
    "beijing-municipal-bureau-of-statistics-01-ls-21-19",
    "beijing-municipal-bureau-of-statistics-01-ls-21-20",
    "beijing-municipal-bureau-of-statistics-01-ls-22-02",
    "beijing-municipal-bureau-of-statistics-01-ls-22-06",
    "beijing-municipal-bureau-of-statistics-01-ls-23-01",
    "beijing-municipal-bureau-of-statistics-01-ls-23-02",
    "beijing-municipal-bureau-of-statistics-01-ls-23-03",
    "beijing-municipal-bureau-of-statistics-01-ls-23-04",
    "beijing-municipal-bureau-of-statistics-01-ls-25-01",
    "beijing-municipal-bureau-of-statistics-01-ls-3-01",
    "beijing-municipal-bureau-of-statistics-01-ls-3-02",
    "beijing-municipal-bureau-of-statistics-01-ls-3-04",
    "beijing-municipal-bureau-of-statistics-01-ls-3-08",
    "beijing-municipal-bureau-of-statistics-01-ls-3-09",
    "beijing-municipal-bureau-of-statistics-01-ls-3-10",
    "beijing-municipal-bureau-of-statistics-01-ls-3-11",
    "beijing-municipal-bureau-of-statistics-01-ls-4-01",
    "beijing-municipal-bureau-of-statistics-01-ls-4-01-1",
    "beijing-municipal-bureau-of-statistics-01-ls-4-02",
    "beijing-municipal-bureau-of-statistics-01-ls-4-03",
    "beijing-municipal-bureau-of-statistics-01-ls-4-04",
    "beijing-municipal-bureau-of-statistics-01-ls-4-05",
    "beijing-municipal-bureau-of-statistics-01-ls-4-06",
    "beijing-municipal-bureau-of-statistics-01-ls-4-07",
    "beijing-municipal-bureau-of-statistics-01-ls-4-08",
    "beijing-municipal-bureau-of-statistics-01-ls-5-01",
    "beijing-municipal-bureau-of-statistics-01-ls-5-02",
    "beijing-municipal-bureau-of-statistics-01-ls-5-03",
    "beijing-municipal-bureau-of-statistics-01-ls-5-04",
    "beijing-municipal-bureau-of-statistics-01-ls-5-05",
    "beijing-municipal-bureau-of-statistics-01-ls-5-06",
    "beijing-municipal-bureau-of-statistics-01-ls-5-07",
    "beijing-municipal-bureau-of-statistics-01-ls-5-08",
    "beijing-municipal-bureau-of-statistics-01-ls-5-09",
    "beijing-municipal-bureau-of-statistics-01-ls-5-10",
    "beijing-municipal-bureau-of-statistics-01-ls-5-11",
    "beijing-municipal-bureau-of-statistics-01-ls-5-16",
    "beijing-municipal-bureau-of-statistics-01-ls-5-17",
    "beijing-municipal-bureau-of-statistics-01-ls-5-18",
    "beijing-municipal-bureau-of-statistics-01-ls-6-01",
    "beijing-municipal-bureau-of-statistics-01-ls-6-01-1",
    "beijing-municipal-bureau-of-statistics-01-ls-6-02",
    "beijing-municipal-bureau-of-statistics-01-ls-6-03",
    "beijing-municipal-bureau-of-statistics-01-ls-6-04",
    "beijing-municipal-bureau-of-statistics-01-ls-6-05",
    "beijing-municipal-bureau-of-statistics-01-ls-6-06",
    "beijing-municipal-bureau-of-statistics-01-ls-6-06-1",
    "beijing-municipal-bureau-of-statistics-01-ls-6-07",
    "beijing-municipal-bureau-of-statistics-01-ls-6-08",
    "beijing-municipal-bureau-of-statistics-01-ls-6-10",
    "beijing-municipal-bureau-of-statistics-01-ls-6-12",
    "beijing-municipal-bureau-of-statistics-01-ls-6-13",
    "beijing-municipal-bureau-of-statistics-01-ls-6-16",
    "beijing-municipal-bureau-of-statistics-01-ls-7-04",
    "beijing-municipal-bureau-of-statistics-01-ls-7-05",
    "beijing-municipal-bureau-of-statistics-01-ls-7-06",
    "beijing-municipal-bureau-of-statistics-01-ls-7-07",
    "beijing-municipal-bureau-of-statistics-01-ls-7-08",
    "beijing-municipal-bureau-of-statistics-01-ls-7-09",
    "beijing-municipal-bureau-of-statistics-01-ls-7-10",
    "beijing-municipal-bureau-of-statistics-01-ls-7-10-1",
    "beijing-municipal-bureau-of-statistics-01-ls-7-12",
    "beijing-municipal-bureau-of-statistics-01-ls-8-01",
    "beijing-municipal-bureau-of-statistics-01-ls-8-02",
    "beijing-municipal-bureau-of-statistics-01-ls-8-04",
    "beijing-municipal-bureau-of-statistics-01-ls-8-05",
    "beijing-municipal-bureau-of-statistics-01-ls-9-01",
    "beijing-municipal-bureau-of-statistics-01-ls-9-01-1",
    "beijing-municipal-bureau-of-statistics-01-ls-9-02",
    "beijing-municipal-bureau-of-statistics-01-ls-9-02-1",
    "beijing-municipal-bureau-of-statistics-01-ls-9-03",
    "beijing-municipal-bureau-of-statistics-01-ls-9-03-1",
    "beijing-municipal-bureau-of-statistics-01-ls-9-04",
    "beijing-municipal-bureau-of-statistics-01-ls-9-04-1",
    "beijing-municipal-bureau-of-statistics-01-ls-9-05",
    "beijing-municipal-bureau-of-statistics-01-ls-9-06",
    "beijing-municipal-bureau-of-statistics-01-ls-9-08",
    "beijing-municipal-bureau-of-statistics-01-ls-9-08-1",
    "beijing-municipal-bureau-of-statistics-01-ls-9-09",
    "beijing-municipal-bureau-of-statistics-01-ls-9-09-1",
    "beijing-municipal-bureau-of-statistics-01-ls-9-10",
    "beijing-municipal-bureau-of-statistics-01-ls-9-11",
    "beijing-municipal-bureau-of-statistics-01-ls-9-11-1",
    "beijing-municipal-bureau-of-statistics-01-ls-9-12",
    "beijing-municipal-bureau-of-statistics-01-ls-9-13",
    "beijing-municipal-bureau-of-statistics-01-ls-9-14",
    "beijing-municipal-bureau-of-statistics-01-ls-9-15",
    "beijing-municipal-bureau-of-statistics-01-ls-9-15-1",
    "beijing-municipal-bureau-of-statistics-01-ls-9-17",
    "beijing-municipal-bureau-of-statistics-01-ls-9-19",
    "beijing-municipal-bureau-of-statistics-01-ls-9-20",
    "beijing-municipal-bureau-of-statistics-01-ls-9-22",
    "beijing-municipal-bureau-of-statistics-01-ls-9-23",
    "beijing-municipal-bureau-of-statistics-01-ls-9-24",
    "beijing-municipal-bureau-of-statistics-05-1",
}

ANNUAL_MASK_FALLBACKS = {
    # A small set of annual LS reports intermittently returns HTTP 500 from
    # queryRptTimeFreqMask while neighboring reports still publish normally.
    # The data/template calls use these same single annual masks.
    "LS-12-07-1": ["2012"],
    "LS-12-07-2": ["2019"],
    "LS-12-08": ["2011"],
    "LS-17-06": ["2011"],
    "LS-18-26": ["2011"],
    "LS-5-02": ["2011"],
    "LS-5-05": ["2011"],
    "LS-7-13": ["2011"],
}


@transient_retry()
def _get_viewer(report: str, subject: str, sort: str) -> str:
    resp = get(
        VIEWER,
        params={
            "method": "queryHtmlStyle",
            "queryCondition.reportNumber": report,
            "queryCondition.objectType": "04",
            "queryCondition.objectCode": subject,
            "queryCondition.dataSortTypeCode": sort,
            "yhid": "guest",
            "netType": "2",
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _post(action: str, data: dict):
    resp = post(ACTION + action, data=data, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _parse_viewer(viewer_html: str) -> dict | None:
    """Pull reportVersion / departmentCode / freqType / usageType from the
    showSinglereport script tag the report viewer embeds. Returns None when the
    viewer is empty / has no report (a placeholder catalog entry)."""
    m = re.search(r'id="showSinglereport"([^>]*)>', viewer_html)
    if not m:
        return None
    seg = m.group(1)

    def attr(name: str):
        mm = re.search(name + r'\s*=\s*"?([^"\s>]*)"?', seg)
        return mm.group(1) if mm else None

    return {
        "reportVersion": attr("reportVersion"),
        "dept": attr("sourceDepartmentCode"),
        "freqType": attr("collectFrequenceTypeCode"),
        # usageType varies per report (01 historical macro tables, 02 LS-style
        # tables) and drives whether queryRptTimeFreqMask returns any masks at
        # all — it MUST come from the viewer, not be assumed.
        "usageType": attr("usageType") or "01",
    }


def _parse_template(tpl_html: str):
    """Return (labels, datacells, min_row, min_col).

    labels[(row, col)] = cleaned label text; datacells = [(row, col, cell_id)].
    Each ``<td id="td_<col>_<row>">`` either holds a data ``<input metaData=...>``
    or a ``<label>`` of header/indicator text.
    """
    labels = {}
    datacells = []
    for m in re.finditer(r'<td\s+id="td_(\d+)_(\d+)"(.*?)</td>', tpl_html, re.S):
        col = int(m.group(1))
        row = int(m.group(2))
        inner = m.group(3)
        dm = re.search(r'metaData\s*=\s*"([^"]+)"', inner)
        if dm:
            datacells.append((row, col, dm.group(1)))
            continue
        lm = re.search(r"<label[^>]*>(.*?)</label>", inner, re.S)
        if lm:
            txt = html.unescape(re.sub(r"<[^>]+>", "", lm.group(1)))
            txt = txt.replace("\xa0", " ").strip()
            if txt:
                labels[(row, col)] = txt
    if not datacells:
        return labels, datacells, None, None
    return labels, datacells, min(r for r, _, _ in datacells), min(c for _, c, _ in datacells)


def _freq_masks(report: str, sort: str, usage_type: str) -> tuple[list[str], str | None]:
    try:
        resp = _post(
            "queryRptTimeFreqMask",
            {
                "reportDataKeyDTO.reportNumber": report,
                "reportDataKeyDTO.usageType": usage_type,
                "reportDataKeyDTO.dataSortTypeCode": sort,
            },
        )
    except httpx.HTTPStatusError as exc:
        if (
            sort == "01"
            and exc.response.status_code >= 500
            and report in ANNUAL_MASK_FALLBACKS
        ):
            return ANNUAL_MASK_FALLBACKS[report], None
        raise
    blocks = resp.json() or []
    masks = []
    dept = None
    for blk in blocks:
        # Two response shapes: macro reports return {departmentCode, list:[...]};
        # LS-style reports return one object per period with collectFrequenceMask.
        if blk.get("list"):
            masks.extend(blk["list"])
        elif blk.get("collectFrequenceMask"):
            masks.append(blk["collectFrequenceMask"])
        if not dept and blk.get("departmentCode"):
            dept = blk["departmentCode"]
    return masks, dept


def _data_key(report, dept, mask, freq_type, subject, report_version, usage_type) -> dict:
    return {
        "reportDataKeyDTO.reportNumber": report,
        # the data call needs a departmentCode placeholder even when the report
        # exposes none — the platform itself posts the literal string "null".
        "reportDataKeyDTO.departmentCode": dept or "null",
        "reportDataKeyDTO.collectFrequenceMask": mask,
        "reportDataKeyDTO.collectDataVersion": "1",
        "reportDataKeyDTO.collectFrequenceTypeCode": freq_type or "",
        "reportDataKeyDTO.usageType": usage_type,
        "reportDataKeyDTO.objectType": "04",
        "reportDataKeyDTO.objectCode": subject,
        "reportDataKeyDTO.reportVersion": report_version or "",
    }


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    ent = _BY_SPEC[node_id]
    report, subject, sort = ent["report"], ent["subject"], ent["sort"]

    if node_id in UNAVAILABLE_SPEC_IDS:
        save_raw_ndjson(
            [
                {
                    "report_number": report,
                    "subject": subject,
                    "sort": sort,
                    "status": "upstream_unavailable",
                    "detail": (
                        "Source catalog/viewer exists, but the verified REST "
                        "data path returns no publishable observation rows."
                    ),
                }
            ],
            asset,
        )
        return

    # 1. Seed the session and read the report's version/department/frequency.
    viewer = _parse_viewer(_get_viewer(report, subject, sort))
    rows = []
    if viewer is None:
        # Placeholder catalog entry with no actual report behind it — persist an
        # empty asset rather than raising, so one dud entry can't abort the DAG.
        save_raw_ndjson(rows, asset)
        return

    report_version = viewer["reportVersion"]
    freq_type = viewer["freqType"]
    usage_type = viewer["usageType"]

    # 2. Available time masks (+ department, which is missing from collect
    #    metadata for ~half the reports but recoverable from the viewer / mask).
    masks, mask_dept = _freq_masks(report, sort, usage_type)
    dept = viewer["dept"] or mask_dept

    if masks:
        # 3. Template (cell layout) — version-keyed, so fetch once and reuse.
        tpl = _post(
            "updateReportHtml",
            _data_key(report, dept, masks[0], freq_type, subject, report_version, usage_type),
        ).text
        labels, datacells, min_row, min_col = _parse_template(tpl)

        if datacells:
            def left_label(r):
                return " / ".join(
                    labels[(r, c)] for c in range(min_col) if (r, c) in labels
                )

            def top_label(c):
                return " / ".join(
                    labels[(rr, c)] for rr in range(min_row) if (rr, c) in labels
                )

            row_label = {r: left_label(r) for r, _, _ in datacells}
            col_label = {c: top_label(c) for _, c, _ in datacells}

            # 4. Per-mask cell values, joined back to the template positions.
            for mask in masks:
                blocks = _post(
                    "queryReportData",
                    _data_key(report, dept, mask, freq_type, subject, report_version, usage_type),
                ).json()
                for block in blocks or []:
                    for data_row in block.get("data", []):
                        vmap = dict(
                            zip(data_row.get("metaData", []), data_row.get("value", []))
                        )
                        for r, c, cell_id in datacells:
                            v = vmap.get(cell_id)
                            if v is None or str(v).strip() == "":
                                continue
                            rows.append(
                                {
                                    "report_number": report,
                                    "freq_type": freq_type,
                                    "mask": mask,
                                    "indicator": row_label[r],
                                    "col_label": col_label[c],
                                    "value": str(v).strip(),
                                }
                            )

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_one, kind="download") for sid in _BY_SPEC
]
