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
