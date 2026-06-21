"""FTC Do-Not-Call reported call numbers.

The "reported call numbers" subset is the union of the daily complaint-number
CSVs the landing page currently lists (a rolling recent window; full history
would require the rate-limited api.ftc.gov dnc-complaints API). Each row is
tagged with the source file's date.
"""

import re

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import BASE, _full_url, _get_bytes, _parse_csv

DNC_PAGE = BASE + "/policy-notices/open-government/data-sets/do-not-call-data"


def fetch_dnc_daily(node_id: str) -> None:
    """Union the daily Do-Not-Call complaint-number CSVs currently listed on the
    landing page; tag each row with the source file's date."""
    asset = node_id
    html = _get_bytes(DNC_PAGE).decode("utf-8", "replace")
    hrefs = re.findall(
        r'href="([^"]*DNC_Complaint_Numbers_\d{4}-\d{2}-\d{2}\.csv)"', html
    )
    files = list(dict.fromkeys(hrefs))  # dedupe, preserve order
    if not files:
        raise RuntimeError(f"{asset}: no DNC daily files found on {DNC_PAGE}")
    rows = []
    for h in files:
        file_date = re.search(r"(\d{4}-\d{2}-\d{2})", h).group(1)
        for rec in _parse_csv(_get_bytes(_full_url(h))):
            rec["source_file_date"] = file_date
            rows.append(rec)
    if not rows:
        raise RuntimeError(f"{asset}: 0 rows across {len(files)} daily files")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="ftc-dnc-reported-call-numbers", fn=fetch_dnc_daily, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ftc-dnc-reported-call-numbers-transform",
        deps=["ftc-dnc-reported-call-numbers"],
        sql='''
            SELECT
                Company_Phone_Number               AS company_phone_number,
                TRY_CAST(Created_Date AS TIMESTAMP)   AS created_at,
                TRY_CAST(Violation_Date AS TIMESTAMP) AS violation_at,
                Consumer_City                      AS consumer_city,
                Consumer_State                     AS consumer_state,
                Consumer_Area_Code                 AS consumer_area_code,
                Subject                            AS subject,
                Recorded_Message_Or_Robocall       AS robocall,
                CAST(source_file_date AS DATE)     AS source_file_date
            FROM "ftc-dnc-reported-call-numbers"
            WHERE Company_Phone_Number IS NOT NULL AND Company_Phone_Number <> ''
        ''',
    ),
]
